**ORDER BUDDY - Speech to Text Order Assistant**

**AUTHORS:**

Aanchal Samdariya, Karan Gulur Muralidhar, Apoorva Kasoju, Krishna Sai Rohith

**SUMMARY:**

Traditional way of placing an order involves repetitive manual labour, be it giving/taking orders face to face at an eatery or using mobile/web applications for ordering. Leveraging increase in popularity of hands free assistant such as Google Home and Alexa, we enable  conversational agent to work as a Speech-to-text Order Assistant. The user will be given  the ability to navigate through all phases of order management
(i.e., placing an order, modifying the existing order and cancel an item/order), in effect, have a conversation and be able to place an order hands free.The following could be an example of the kind of conversation possible with Order Buddy:
 
OB: Hey there! What do you want to order? 
Cust: I want a Mocha Latte. 
OB: What size? 
Cust: Large 
OB: Got it, one large Mocha Latte. Do you want to order anything else? 
Cust: One small Coffee please. 
OB: Got it, one small Coffee. Do you want to order anything else?
Cust: No, that's it. 
OB: Order for 1 large Mocha Latte and 1 small Coffee is Confirmed, have a good day! 

The history of all orders are stored for future reference and the entire application is integrated with the Google Assistant.A subset of the menu from Starbucks will be used as the dataset for proof of concept and later aim to expand to any menu.

**METHODS:**
On a high level, we have the user who is facing the Google voice assistant. Any utterance emitted by the user to the voice assistant will be converted to text using Google Speech to Text APIs. The text form of the utterance is then forwarded to the chat bot framework (implemented with Dialogflow) which is responsible for intent matching and entity extraction. The request is then forwarded to the back-end code which is responsible for business logic and data storage (Google Cloud Firestore) and the response is returned back to the user.High level architecture is presented below .

![alt text](https://github.com/sairohith07/OrderBuddy/tree/master/images/high_level_arch.png)

- Entity Extraction:In order to identify what a particular user is referring to, our chat bot framework should be able to identify the menu items, size customization parameters a user mentions in the utterance. Even though we have the state of the art entity extractor to identify place, location,and organization words, a custom entity model is developed using DialogFlow Framework,where we can define new entities with a small probable set of values and also give us the flexibility to list synonyms.For this project, we create ’Drinks’, ’Customization’ and ’Size’ entities in Dialogflow. For Ex, an
’large’ is a value mentioned under the entity ’Size’ with synonyms ’huge’ and ’Venti’.
- Intent Identification and Training:Every user utterance should be analysed mapped to a particular action - order, cancel_item, cancel_order, complete_order. The process of mapping an user utterance to a corresponding action is called as intent identification.In DialogFlow , we define intents along with sample training phrases.We also make sure to diverge the sentence structure required to trigger an intent and restrict the flow of conversation amongst intents to avoid any situation that might lead to a one-to-many intent matching.
- Google Cloud Firestore: The Cloud Firestore.a No-SQL database, is used to handle and store all the customer’s current and past orders using two collections , history and current_order.Order onces processed and complete are moved from current_order to history.
- Intent Transition:To achieve intent matching, four main intents are implemented which is Order Intent (to add an item in the cart), Cancel Item Intent (to can- cel a previously ordered item), Cancel Order intent (to cancel the entire order) and Complete Order Intent (to complete/place an order).Any intent can be called at any point of the conversation depending on the user’s utterance and transition between intents can be seen in below figure.
![alt text](https://github.com/sairohith07/OrderBuddy/tree/master/images/State_Transition.png)

- Integration with Google Assistant: To invoke our application from Google Assistant there are essentially using explicit and implicit invocation ,by mapping to intents in the DialogFlow agent.To integrate Google Actions with the chat bot developed using Dialogflow, an intent with event Google_Action_Welcome needs to be defined. When the end-user triggers our application with invocation, the con- text of our chat bot is invoked using this intent and from then on-wards every ut- terance is with the chat bot until the end of conversation.
- Personalization:In order to provide customized recommendations for a repeat cus- tomer or just to address a new customer by his name in his next interaction with our ap- plication, we need to know his identity via primarily using ’Account Creation’.We decided to use Google for this task, where the conversation control momentarily transitions into Google’s environment to extract basic user information such as name or email, achieved using Helper intents from Action on Google developer platform .


**TESTING and RESULTS:**
A sample conversation in below figure shows the transition of intents based on user’s utterances and context mapping, along with responses.As seen in the figure mentioned, a typical user wishes to have a small coffee in first figure of the flow. Upon receiving user’s voice input, it is converted to text. The intent is identified and agent looks for required entities to fulfill the order and hence prompts the user to specify, i.e., customization (second figure in the flow). Once the slot-filling (required entities) is accomplished, the Firestore is updated with the current order information for the user as part of the business logic and the user is notified about the same, including in response if he wants to add anything more. 
The user adds another drink to the order (third figure in the flow), without any customization (fourth figure in the flow). Again the user is asked if they would like to add to the order. Here, the user does not want to add anything else to their order, which results in completion of the entire order of which the user is notified (fifth figure in the flow).

![alt text](https://github.com/sairohith07/OrderBuddy/tree/master/images/order_flow_2.png)

In order to evaluate how well the the voice based ordering system is performing, two main functionalities - intent detection and entity extraction were tested.A set of testing phrases consisting of all possible intents and entities had to be formu- lated along with the golden truth. In order to avoid bias in testing phrases, following were the different techniques used in collection of intent phrases.
- Manual collection from a coffee shop
- TaskMaster dataset,consisting of 13,215 task-based dialogues in English, including 5,507 spoken and 7,708 written dialogues,from which dialogues corresponding to ordering coffee were extracted
- Responses collected through friends and family to obtain their usual way of ordering coffee by using Google Forms

An automated testing framework which acts a client for the chat bot framework was developed in python using Pytest which takes in testing phrases formulated above and validates with the golden truth output.
Testing results can have two kind of errors broadly: 
- Intent Error: The detected intent is not same as the golden truth intent 
- Entity Error: Intent detection is right but entity detection - drink, size, customize parameter is wrong.

Each intent is evaluated separately and the number for training and testing phrases used for evaluation of each intent along with the accuracy scores for Order intent without/with customization are 88.54% and 87.89% respectively. These errors were mainly entity recognition errors with no intent recognition errors. Cancel intent received a slightly lower accuracy of 83.44\%. This was again due to the entity recognition errors mainly. Cancel order and Complete order intents have received very high accuracy of 96% and 100% respectively. 
The reason is that we have reserved phrases for each of these intents to be recognized which are 'Abort' for Cancel order and 'Complete order' for Complete order intent to be recognized. There are no entities required to be identified for these intents, resulting in such high accuracy.



**DISCUSSIONS**

The results obtained show that we have managed to develop an application to provide the basic functionalities for a speech to text order.Our future work will include below developments:

- Increase training for intents
- Modification of existing order to allow user to change order at anytime during order lifecycle.
- Expand application to include multiple Items and Restaurants
- Allowing more personalized experience to customer on his next visit


**REFERENCES :**

\[1\] **Google Speech-to-text API** : *https://cloud.google.com/speech-to-text/*.

\[2\] **Google Cloud Natural Language** :*https://cloud.google.com/natural-language/*.

\[3\] **Homa B. Hashemi, and Amir Asiaee, Reiner Kraft**
***Query Intent Detection using Convolutional Neural Networks*** 
Systems Intelligent Systems Program,University of Pittsburg and Yahoo
Inc.,Sunnyvale,CA

\[4\] **Google Cloud DialogFlow** : *https://cloud.google.com/dialogflow/docs/reference/rest/v2- overview*.

\[5\] **Brenes, David Gayo-Avello, Daniel and Pérez-González, Kilian** 
***Survey and evaluation of query intent detection methods*** 
Proceedings of Workshop on Web Search Click Data, WSCD’09.
10.1145/1507509.1507510
