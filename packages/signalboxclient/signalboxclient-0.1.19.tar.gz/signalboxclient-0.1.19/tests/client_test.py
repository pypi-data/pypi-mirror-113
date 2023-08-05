from context import signalboxclient
# import client
import datetime
import random
import uuid
import numpy as np
import environment

creds = signalboxclient.client.Credentials(environment.api_key)
test_client = signalboxclient.client.SignalBoxClient(creds)

my_token = test_client.access_token
# create user
user_id = str(uuid.uuid1())
u = test_client.create_user('testuser', user_id)
print('created user with id=', user_id)
# update the user
u['properties'] = {
    'client_test.py': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
}
test_client.create_or_update_users([u])
offer = test_client.create_offer('my_offer', 'AUD', 100, 50)
offer_id = offer['id']

# create a touchpoint
touchpoint_id = "client_test.py"
tp = test_client.create_touchpoint_on_tracked_user(
    user_id, touchpoint_id, {"key": "value"})

assert tp['version'] > 0
touchpoint_id = "client_test.py"
tp = test_client.get_touchpoint_on_tracked_user(
    user_id, touchpoint_id)

assert tp["values"]["key"] == "value"
# get the touchpoint
touchpoint = test_client.get_touchpoint(touchpoint_id)
assert touchpoint['commonId'] == touchpoint_id

# create a product
product_id = str(uuid.uuid1())
product = test_client.create_product(
    product_id, "client_test.py Product", 10, None, "A test description.")
assert product['id'] > 0

# # query the products
response = test_client.query_products(page=1)
assert len(response.items) > 1

# create a product recommender
product_recommender_id = str(uuid.uuid1())
product_recommender = test_client.create_product_recommender(
    product_recommender_id, "client_test.py Recommender", touchpoint_id)
assert product_recommender['id'] is not None

for i in range(1, 10):
    start = datetime.datetime(2020, i, 1).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    end = datetime.datetime(2020, i+1, 1).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    test_client.create_product_recommender_target_variable_value(
        product_recommender['id'], start, end, "LTV", i * 7 * random.randint(1, 3))

target_variable_values = test_client.get_product_recommender_target_variable_values(product_recommender_id)
assert len(target_variable_values) > 0

# delete the recommender
delete_response = test_client.delete_product_recommender(
    product_recommender['id'])
assert delete_response['id'] is not None


# create a parameter
parameter_id = str(uuid.uuid1())
parameter = test_client.create_parameter(
    common_id=parameter_id, name="client_test.py")
assert parameter['id'] is not None
assert parameter['commonId'] == parameter_id
print("Created Parameter")

# create a feature
feat_id = f'client.py-{uuid.uuid1()}'
feat = test_client.create_feature(feat_id, "Python Client Feature")
feat_r = test_client.get_feature(feat_id)
assert feat_r['id'] == feat['id']
# check we can set a feature and get a feature on a user
test_client.set_feature_value(user_id, feat_id, 5)
feature_value = test_client.get_feature_value(user_id, feat_id)
assert feature_value['value'] == 5
print('tracked user with feature value:', user_id)

experiment = test_client.create_experiment(
    [offer_id], name='Experiment Name', segment_id=None, concurrent_offers=1)
print('created experiment')
experiment_id = experiment['id']

# list all experiments
experiments_first_page = test_client.query_experiments(1)
print('len experiments_first_page =', len(experiments_first_page.items))
assert experiments_first_page.pagination.totalItemCount > 0

get_experiment_response = test_client.get_experiment(experiment_id)
print('\nPrinting get_experiment test response: ', get_experiment_response)

offers_in_experiment = test_client.get_offers_in_experiment(experiment_id)
assert offers_in_experiment is not None
assert len(offers_in_experiment) > 0

print('\nPrinting create_offer test response: ', offer)
print('\nPrinting create_experiment test response: ', experiment)

recommended_offer = test_client.recommend_offer(experiment_id, user_id)
assert recommended_offer['recommendationCorrelatorId'] is not None

# create an event with the correlatorId in it
e = test_client.construct_event(user_id, str(uuid.uuid1()), "TestOffer", "ViewOffer", {
}, None, None, recommended_offer['recommendationCorrelatorId'])
test_client.log_events([e])

# choose accept or rekect
tracked = test_client.track_recommendation_outcome(
    recommended_offer, recommended_offer['offers'][0]['id'], 'accept')
print(tracked)

event_types = ["CREATED", "CANCELED"]
event_kinds = ["BILLING", "TICKET"]
events = []
for i in range(100):
    uid = str(uuid.uuid1())
    print(f'Event User Id: ', uid)
    events.append(test_client.construct_event(
        uid, str(uuid.uuid1()), np.random.choice(event_types), np.random.choice(event_kinds), {}))
    # commonUserId, event_id, event_type, kind, properties, timestamp, source_system_id

print(f'logging {len(events)} events')
result = test_client.log_events(events)
print(result)

print('\ntests successful')
