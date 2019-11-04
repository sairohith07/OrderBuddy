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

As of now, the above conversation has been accomplished. To achieve this, we have business logic to handle four different intents - Order intent, Cancel Item intent, Cancel Order intent and Complete order intent.
The current and history of all orders are stored for future reference in the Google's Firestore database. A subset of the menu from Starbucks is used as the dataset for our project. 

As part of further enhancements, we would like to include more intents for example, to handle modification to orders. We would also want to improve the intent identification model and integrate our service with third-party assistants, which is explained in more detail in the below section.

**PROPOSED PLAN OF RESEARCH:**

In the initial phase of the presentation, a basic implementation of entity identification and state transitions is handled with the help of Google Cloud Dialogflow and Firestore services and business logic code. A user will be able to have a conversation with the order buddy bot and order multiple items at a restaurant.

For the second phase of the project, we would like to extend the functionality of the basic bot and also make it error-free. The following are some of the additional features considered.

- We will enable the bot to support additional intents like modify intent (add customization to each item).
- The model is to be improved in order to identify intents more efficiently. This we plan to achieve by enlarging the training set of phrases used to identify each intent.
- Integration of our service with third-party agents such as Google Assistant, Phone or FB messenger will be enabled.
- We want to enable this service to support multiple restaurants instead of just a single one.
- Convert menu image to text to simplify the process of defining the entity for each restaurant.

To evaulate the system, we plan to prepare a Goggle survey to collect a variety of examples for each intent and test these examples against our service. We will calculate F1-score for each intent to evaluate our service.

**PRELIMNARY RESULTS:**

The image below represents sample conversation using our agent.

![alt text](https://github.com/sairohith07/OrderBuddy/blob/master/images/Complete_conversation.png)

A sample conversation in above figure  shows the transition of intents based on user's utterances and context mapping, along with responses.
As seen in the figure mentioned, a typical user wishes to have a small coffee in first figure of the flow. Upon receiving user's voice input, it is converted to text. The intent is identified and agent looks for required entities to fulfill the order and hence prompts the user to specify, i.e., size(second figure in the flow). Once the slot-filling(required entities) is accomplished, the Firestore database is updated with the current order information for the user as part of the business logic and the user is notified about the same (third figure in the flow), including in response if he wants to add anything more.
Here, the user expresses his intent to cancel one of items(fourth figure in the flow), for which the follow-up intent is triggered and the agent responds by providing options for the user to choose for cancel. After the user provides the option, the agent confirms the cancellation and prompts user to choose to continue or complete the order(fifth figure in the flow).
If the user wishes to complete the order, the agent prompts to confirm to place the order and a positive response results in placing/completing the order(sixth figure).


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
