A small python tool to extract data from json files. Makes use of several recusive functions to navigate through the json structure.

## Usage
from JPrune import JPrune

jp = JPrune("tests/test_data.json")

## sorted(jp.get_paths(jp.data))

['project', 'project.auditTrail', 'project.auditTrail.events', 'project.auditTrail.events.actor', 'project.auditTrail.events.changes', 'project.auditTrail.events.changes.field', 'project.auditTrail.events.changes.from', 'project.auditTrail.events.changes.to', 'project.auditTrail.events.message', 'project.auditTrail.events.message.context', 'project.auditTrail.events.message.context.documentId', 'project.auditTrail.events.message.context.line', 'project.auditTrail.events.message.context.suggestedFix', 'project.auditTrail.events.message.context.suggestedFix.action', 'project.auditTrail.events.message.context.suggestedFix.target', 'project.auditTrail.events.message.text', 'project.auditTrail.events.timestamp', 'project.auditTrail.events.type', 'project.config',  
... etc ...]

## jp.show_paths()

project  
project.auditTrail  
project.auditTrail.events  
project.auditTrail.events.actor  
project.auditTrail.events.changes  
project.auditTrail.events.changes.field  
project.auditTrail.events.changes.from  
project.auditTrail.events.changes.to  
project.auditTrail.events.message  
project.auditTrail.events.message.context  
project.auditTrail.events.message.context.documentId  
project.auditTrail.events.message.context.line  
project.auditTrail.events.message.context.suggestedFix  
project.auditTrail.events.message.context.suggestedFix.action  
project.auditTrail.events.message.context.suggestedFix.target  
project.auditTrail.events.message.text  
project.auditTrail.events.timestamp  
project.auditTrail.events.type  
project.config  
... etc ...

## jp.show_schema()

{
  "project": {
    "auditTrail": {
      "events": {
        "changes": {
          "to": "str"
        },
        "message": {
          "context": "str"
        }
      }
    },
    "data": {
      "documents": {
        "synopsis": "str"
      },
      "notes": {
        "note": "str"
      }
    },
    "meta": {
      "owner": {
        "contact": {
          "slack": "str"
        }
      }
    }
  }
}

## jp.find_key('title')

['data.documents.title']

## jp.get_value_by_path(jp.data, 'data.documents.title')

['Natural language processing', 'Machine learning models', 'Knowledge graph models', 'Text Classification']

## jp.paths_to_structure(['data.documents.title','data.documents.synopsis'])

{'data': {'documents': {'title': {}, 'synopsis': {}}}}

## jp.filter(keep_paths=['project.data.documents.title','project.data.documents.synopsis'])

filtered = jp.filter(keep_paths=['project.data.documents.title','project.data.documents.synopsis'])

{
  "project": {
    "data": {
      "documents": [
        {
          "title": "Natural language processing",
          "synopsis": "This document introduces the concept of Natural Language Processing (NLP), focusing on how machines parse and interpret human language. It provides a foundational understanding of textual analysis in computational systems."
        },
        {
          "title": "Machine learning models",
          "synopsis": "This document discusses the requirements for training machine learning models in NLP tasks, emphasizing the need for annotated corpora to enable accurate learning and performance in real-world applications."
        },
        {
          "title": "Knowledge graph models",
          "synopsis": "This document explores the role of knowledge graphs in representing semantic relationships between entities. It emphasizes their utility in improving search relevance, data linking, and reasoning within AI-driven systems."
        },
        {
          "title": "Text Classification",
          "synopsis": "This document outlines the principles of text classification as a supervised learning task. It explains how models are trained on labeled data to automatically categorize new textual inputs based on learned patterns."
        }
      ]
    }
  }
}

## jp.collapse_to_string(filtered, sep='\n')

Natural language processing  
This document introduces the concept of Natural Language Processing (NLP), focusing on how machines parse and interpret human language. It provides a foundational understanding of textual analysis in computational systems.  
Machine learning models  
This document discusses the requirements for training machine learning models in NLP tasks, emphasizing the need for annotated corpora to enable accurate learning and performance in real-world applications.  
Knowledge graph models  
This document explores the role of knowledge graphs in representing semantic relationships between entities. It emphasizes their utility in improving search relevance, data linking, and reasoning within AI-driven systems.  
Text Classification  
This document outlines the principles of text classification as a supervised learning task. It explains how models are trained on labeled data to automatically categorize new textual inputs based on learned patterns.

## jp.extract_text(jp.data, ['project.data.documents.title','project.data.documents.synopsis'])

Accomplishes the same as combining the two functions above, filter and collapse to string.