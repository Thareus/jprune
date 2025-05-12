A small python tool to extract data from json files. Makes use of several recusive functions to navigate through the json structure.

## Usage
from JPrune import JPrune

jp = JPrune("tests/test_data.json")

## jp.get_paths(jp.data)

{'project.auditTrail', 'project.data.documents.metadata.length', 'project.data.notes.deep.nested.tags', 'project.data.documents.doc_id', 'project.meta.owner', 'project.meta.tags.dynamic', 'project.config.processing', 'project.meta.status', 'project.auditTrail.events.actor', 'project.config.processing.features.tokenization.lang', 'project.config.processing.features.tokenization', 'project.config', 'project.auditTrail.events.message.context.line', 'project.data.documents', 'project.config.processing.retryPolicy', 'project.config.processing.enableCache', 'project.auditTrail.events.message', 'project.data.documents.metadata.revisions', 'project.meta.owner.contact.email', 'project.data.notes.deep.nested', 'project.config.processing.retryPolicy.maxRetries', 'project.auditTrail.events.message.text', 'project.meta.created', 'project.auditTrail.events.message.context.documentId', 'project.meta.owner.name', 'project.auditTrail.events', 'project.meta', 'project.data.notes.deep', 'project.data.documents.chapters', 'project.data.notes.deep.nested.comment', 'project.data.documents.metadata.flags.flagged', 'project.config.processing.features', 'project.auditTrail.events.message.context.suggestedFix', 'project.id', 'project.data.documents.metadata', 'project.auditTrail.events.changes.from', 'project.meta.owner.contact', 'project.config.processing.features.entityRecognition', 'project.data.documents.title', 'project.meta.owner.contact.subscribed', 'project.data.documents.metadata.language', 'project.data.documents.metadata.flags', 'project.config.processing.features.tokenization.enabled', 'project.config.processing.features.entityRecognition.enabled', 'project.data', 'project.data.notes.resolved', 'project.auditTrail.events.type', 'project.config.processing.retryPolicy.backoff.initialDelayMs', 'project.auditTrail.events.message.context.suggestedFix.action', 'project.auditTrail.events.changes.field', 'project.auditTrail.events.timestamp', 'project.config.processing.retryPolicy.backoff', 'project.auditTrail.events.message.context.suggestedFix.target', 'project.data.notes', 'project.config.processing.retryPolicy.backoff.strategy', 'project.data.notes.priority', 'project.data.documents.metadata.flags.reviewed', 'project.auditTrail.events.changes', 'project.meta.tags', 'project', 'project.auditTrail.events.changes.to', 'project.data.documents.synopsis', 'project.meta.owner.contact.slack', 'project.data.notes.note', 'project.auditTrail.events.message.context'}


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
project.config.processing
project.config.processing.enableCache
project.config.processing.features
project.config.processing.features.entityRecognition
project.config.processing.features.entityRecognition.enabled
project.config.processing.features.tokenization
project.config.processing.features.tokenization.enabled
project.config.processing.features.tokenization.lang
project.config.processing.retryPolicy
project.config.processing.retryPolicy.backoff
project.config.processing.retryPolicy.backoff.initialDelayMs
project.config.processing.retryPolicy.backoff.strategy
project.config.processing.retryPolicy.maxRetries
project.data
project.data.documents
project.data.documents.chapters
project.data.documents.doc_id
project.data.documents.metadata
project.data.documents.metadata.flags
project.data.documents.metadata.flags.flagged
project.data.documents.metadata.flags.reviewed
project.data.documents.metadata.language
project.data.documents.metadata.length
project.data.documents.metadata.revisions
project.data.documents.synopsis
project.data.documents.title
project.data.notes
project.data.notes.deep
project.data.notes.deep.nested
project.data.notes.deep.nested.comment
project.data.notes.deep.nested.tags
project.data.notes.note
project.data.notes.priority
project.data.notes.resolved
project.id
project.meta
project.meta.created
project.meta.owner
project.meta.owner.contact
project.meta.owner.contact.email
project.meta.owner.contact.slack
project.meta.owner.contact.subscribed
project.meta.owner.name
project.meta.status
project.meta.tags
project.meta.tags.dynamic

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