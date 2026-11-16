## Part 3. Initial AI Implementation

### 3.1. Proposed AI Feature

Our AI feature is an apartment evaluation system that helps users decide whether an apartment is a good fit for them.

The system looks at apartment details and compares them with the user's housing preferences. Using this information, the AI provides a personalized rating & explanation. Users can also enter their own questions or prompts about specific things they care about, like amenities, location, or access to public transportation.

### 3.2. Proposed AI Model and Technique

We are currently using **Qwen2.5:3b**, a language model that runs locally through **Ollama**.

Instead of training our own AI model, we use prompt engineering. This means we give the model apartment information, user preferences, and instructions on how to evaluate the apartment.

We chose to run the model locally because it allows us to test AI features without depending on a paid external AI service. It also gives us more control over how the application handles user and apartment information.

### 3.3. Input and Output

**Input:**

The AI uses 3 main types of information:

- **User preferences:** Preferences saved in the user's account, such as their budget and housing needs.
- **Apartment details:** Apartment information retrieved from our SQLite database.
- **Additional user input:** Questions or instructions entered by the user to focus on specific things they care about, such as amenities, location, or transportation.

**Output:**

The model returns a response in JSON format with three main parts:

- **Rating:** A score out of 5 based on how well the apartment matches the user's preferences and input.
- **Summary:** A short overview of the apartment and how well it fits the user's needs.
- **Reasoning:** An explanation of why the apartment received that rating.

Using JSON makes it easier for Django to process the model's response and display the results in a consistent format.

### 3.4. Interaction with Django

Django connects the application, database, and AI model. The process works as follows:

1. The user selects an apartment and requests an AI evaluation.
2. Django retrieves the user's saved preferences and the apartment details from the SQLite database.
3. The application also collects any additional prompt or questions entered by the user.
4. Django combines the apartment information, user preferences, and additional input into a prompt for the AI model.
5. Django sends the prompt to Qwen2.5:3b through Ollama, which runs locally on the machine.
6. Qwen processes the information and returns an evaluation in JSON format.
7. Django checks whether the response contains valid JSON. If everything looks correct, the evaluation is displayed to the user. If something goes wrong, the application displays an error message and asks the user to try again.

Ollama acts as the connection between Django and the locally hosted Qwen model. Django handles the database operations, user input, and processing of the model's response.

### 3.5. Initial Experimentation and Technical Feasibility

We have successfully set up Ollama locally and connected Qwen2.5:3b to our Django application. Our initial implementation shows that Django can collect apartment details and user preferences, send that information to the AI model, and receive an evaluation.

We also added JSON validation to check the model's responses. This helps prevent invalid / incorrectly formatted results from being displayed to users.

So far, our prototype shows that using a locally hosted AI model in our Django application is possible. We may also test Qwen2.5:1b to see how it compares in terms of response quality & computer resource usage.

**Current Limitations and Future Improvements:**

- The quality of the AI evaluation depends on how accurate & complete the apartment information in our database is.
- The model may give different responses depending on the information and instructions it receives.
- We still need to test how accurate and useful the evaluations are, as well as how long the model takes to respond.
- We may compare different Qwen model sizes to find one that provides good results without requiring too many computer resources.
