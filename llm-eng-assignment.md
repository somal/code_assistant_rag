# LLM Engineer Candidate Assignment: Ultralytics Code Assistant

## Overview
Build a simple code assistant that answers questions about Ultralytics YOLO by retrieving relevant source code and generating helpful responses.

## Time Commitment
- **Expected effort**: 5-10 hours
- **Deadline**: 1 week from assignment date

## What to Build

### Core Features
1. **Chat Interface**: Simple Gradio or Streamlit app for Q&A
2. **Code Indexing**: Index Python files from `ultralytics/models/`, `ultralytics/engine/`, `ultralytics/data/`
3. **Vector Search**: Store and retrieve code chunks using MongoDB Atlas
4. **Answer Generation**: Use a free OpenRouter model to generate responses

### Technical Requirements
- **Environment**: Use `uv` for package management
- **Dependencies**: Define in `pyproject.toml`
- **Embeddings**: Any open-source model (explain your choice)
- **LLM**: Any free OpenRouter model or your preference (explain your choice)
- **Constraints**: No pre-built RAG frameworks (LangChain, LlamaIndex, etc.)

## Deliverables

1. **GitHub Repository** with:
   - Working code
   - Clear README with setup instructions
   - 3-5 example questions from real YOLO use cases
   - Brief design documentation

2. **Design Notes** (in README):
   - How you chunk code and why
   - What metadata you extract
   - Your model choices and rationale
   - Trade-offs you made

3. **Future Work Section**:
   - What would you improve with more time?
   - How would this scale to production?
   - Any critical missing features?

## Evaluation Criteria

- **Implementation** (40%): Code quality, design decisions, understanding of fundamentals
- **Functionality** (30%): Does it work? Are answers reasonable?
- **Documentation** (30%): Clear instructions, thoughtful design notes, vision for improvements

## Important Notes
- MongoDB Atlas offers free tier with vector search support
- Focus on demonstrating your problem-solving approach

## Submission
- Share your public GitHub repository URL
- Include a screenshot of your working demo
- Ensure someone can run your code by following your README