## Part 3. Initial AI Implementation

### 3.1. Proposed AI Feature

Our planned AI feature is an apartment evaluation system that helps users determine how well an apartment matches their housing preferences and needs.

The system uses a language model to analyze apartment information alongside user preferences and provide a personalized evaluation. Users can also enter an additional prompt to ask about specific factors, such as apartment amenities, location, or transportation accessibility.

### 3.2. Proposed AI Model and Technique

We are currently using **Qwen2.5:3b**, a locally hosted language model accessed through **Ollama**.

Our approach relies on prompt engineering rather than additional model training or fine-tuning. The task involves evaluating structured apartment information against user preferences, so we provide the model with relevant information and instructions through a carefully constructed prompt.

We chose a locally hosted model because it allows us to experiment with AI functionality without relying on an external paid AI API. It also gives us more control over how user and apartment information is processed.

### 3.3. Input and Output

**Input:**
- User preferences stored in their account.
- Apartment information retrieved from the SQLite database.
- Additional questions or instructions entered by the user.

**Output:**

The model returns a JSON-formatted response containing:
- **Rating:** A score out of 5 indicating how well the apartment matches the user's preferences.
- **Summary:** A brief overview of the apartment's suitability.
- **Reasoning:** An explanation of why the apartment received that rating.

This structured output allows Django to process and display the AI evaluation in a consistent format.

### 3.4. Interaction with Django

Django manages communication between the application, database, and AI model.

The workflow is as follows:

1. The user selects an apartment and requests an AI evaluation.
2. Django retrieves the user's preferences and the apartment information from the SQLite database.
3. The Django view combines this information with the user's additional prompt to construct an instruction for the model.
4. Django sends the prompt to Ollama's chat endpoint, where Qwen2.5:3b processes the request.
5. Qwen returns a response in JSON format.
6. Django checks whether the response contains valid JSON. If valid, the evaluation is displayed to the user. If the response is invalid or the request fails, the application displays an error message asking the user to try again.

Django's ORM is used for database operations, which helps protect against common SQL injection risks when queries are constructed properly. Django also handles the application-side input and output processing.

### 3.5. Initial Experimentation and Technical Feasibility

We have set up Ollama locally and connected the Qwen2.5:3b model to our Django application. Our initial implementation demonstrates that Django can collect the necessary apartment and user information, send it to the model, and process its response.

We also implemented JSON validation so that the application can handle unexpected or improperly formatted model responses instead of displaying invalid results directly.

This initial prototype demonstrates the feasibility of incorporating a locally hosted language model into our Django application. We may also experiment with Qwen2.5:1b to compare performance and resource requirements.

**Current Limitations and Future Improvements:**

- AI evaluations depend on the accuracy and completeness of the apartment information stored in our database.
- Model responses may vary in quality depending on the prompt and available information.
- We plan to evaluate response quality, accuracy, and latency to determine whether the current model is suitable for our application.
- We may compare different Qwen model sizes to find a balance between response quality and computational requirements.
