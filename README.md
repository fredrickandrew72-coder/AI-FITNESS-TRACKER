# AI Fitness & Nutrition Assistant

> A multimodal, context-aware AI system for food recognition, nutrition analysis, fitness tracking, and personalized dietary recommendations for college and hostel students.

**Project Status:** 🚧 In Development  
**Current Completed Stage:** Food Detection Model Development and Evaluation

---

## 📌 Project Overview

The **AI Fitness & Nutrition Assistant** is an AI-based system designed to help college and hostel students monitor their food intake, understand nutrition, track fitness-related information, and receive personalized dietary recommendations.

The system is designed around a practical problem faced by students: food is often consumed from hostel messes, college canteens, restaurants, and outside-food sources, making accurate and consistent food logging difficult.

Instead of requiring users to manually search for every food item and enter its nutritional information, the proposed system aims to understand food through **images and natural-language input**, retrieve relevant nutritional information, consider the user's fitness goals and activity, and provide personalized recommendations.

The project combines:

- Computer Vision
- Food Object Detection
- Vision-Language Models (VLM)
- Natural Language Processing
- Nutrition Knowledge Retrieval
- Retrieval-Augmented Generation (RAG)
- Machine Learning
- Personalized Recommendation

The current development stage focuses on the **food detection component**, where multiple YOLO models have been trained and experimentally evaluated.

---

# 🎯 Problem Statement

Maintaining a proper diet and fitness routine can be difficult for college and hostel students.

Students frequently depend on:

- Hostel/mess food
- College canteens
- Restaurants
- Fast food
- Outside food
- Frequently changing menus

Existing calorie-counting and nutrition applications often depend heavily on manual food entry. Users may need to search for the food item, determine the quantity, and enter nutritional information themselves.

This creates several challenges:

- Manual food logging is time-consuming.
- Indian and regional foods may not always be represented accurately.
- Students may not know the nutritional composition of their meals.
- Hostel and mess menus change frequently.
- Food consumed outside the hostel may be difficult to log.
- Nutrition information is often separated from fitness activity and user goals.
- Generic recommendations may not account for individual requirements.

### Proposed Problem

The project aims to develop an intelligent system that can automatically understand food inputs, retrieve nutritional information, consider user context and fitness goals, and provide personalized nutrition assistance.

The system therefore investigates the following research direction:

> **Can a multimodal AI system combine food image understanding, nutrition knowledge retrieval, user context, and fitness information to provide practical and personalized nutrition assistance for college and hostel students?**

---

# 💡 Proposed Solution

The proposed system follows a multimodal pipeline where users can provide information through different inputs.

### Possible Inputs

- Food images
- Natural-language food descriptions
- Hostel/mess menu images
- Restaurant or outside-food information
- Fitness/activity information
- User goals and preferences

The system processes these inputs and produces:

- Food identification
- Nutritional information
- Calorie estimation
- Macronutrient information
- Micronutrient information where available
- Personalized nutrition suggestions
- Fitness-oriented food recommendations

### High-Level Architecture

```text
                         USER
                           |
          +----------------+----------------+
          |                |                |
      Food Image       Text Input      Menu Image
          |                |                |
          +----------------+----------------+
                           |
                           v
                  Food Understanding
                           |
              +------------+------------+
              |                         |
         YOLO11s                    VLM/NLP
      Food Detection           Future Integration
              |                         |
              +------------+------------+
                           |
                           v
                  Detected Food Items
                           |
                           v
             Nutrition Knowledge Layer
                  Database + RAG
                           |
                           v
              Nutritional Analysis
                           |
          +----------------+----------------+
          |                |                |
       Calories       Macronutrients   Micronutrients
          |                |                |
          +----------------+----------------+
                           |
                           v
                   User Context
                           |
          +----------------+----------------+
          |                |                |
      Fitness Goal      Activity       Preferences
          |                |                |
          +----------------+----------------+
                           |
                           v
             Personalized Recommendation
                           |
                           v
              AI Fitness Assistant



🧠 AI/ML Approach
The project is designed as a combination of multiple AI components.
1. Food Detection
The first major component is automatic food detection from images.
The current implementation uses YOLO-based object detection.
The following models were trained and compared:
- YOLOv8n
- YOLOv8s
- YOLO11n
- YOLO11s
The models were evaluated using the same experimental protocol to provide a fair comparison.


2. Vision-Language Model
A Vision-Language Model is planned as part of the broader multimodal system for understanding complex food images and menu images.
The VLM component is intended to help with cases where simple object detection may not be sufficient, such as:
- Understanding menu images
- Interpreting food descriptions
- Handling complex meal images
- Extracting contextual information from images
The complete VLM pipeline is part of the future integration stage.

3. Nutrition Knowledge Retrieval
After food items are identified, the system retrieves nutritional information from the project's nutrition data sources.
The nutrition layer is intended to provide information such as:
- Calories
- Protein
- Carbohydrates
- Fat
- Fiber
- Micronutrients
Processed nutrition datasets are already included in the project.
