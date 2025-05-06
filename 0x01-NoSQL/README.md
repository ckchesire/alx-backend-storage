
# Introduction to MongoDB and NoSQL

This document provides a concise overview of NoSQL databases, with a focus on MongoDB. It covers fundamental concepts, differences between SQL and NoSQL, core features of document stores, and practical MongoDB usage for backend development.

## What is NoSQL?

NoSQL stands for "Not Only SQL". It refers to a category of databases that move away from the traditional relational model, offering flexibility in schema design, high scalability, and optimized performance for large-scale and real-time applications.

## Key Differences: SQL vs NoSQL

| Feature           | SQL (Relational)               | NoSQL (Non-relational)           |
|-------------------|--------------------------------|----------------------------------|
| Structure         | Tables with fixed schemas      | Flexible JSON-like documents     |
| Schema            | Strict schema enforcement      | Dynamic/flexible schema          |
| Scaling           | Vertical                       | Horizontal                        |
| Joins             | Supported                      | Often avoided                    |
| ACID Compliance   | Strong                         | Varies (MongoDB supports it)     |
| Use Cases         | Banking, enterprise systems    | Web apps, big data, IoT          |

## What is ACID?

ACID is a set of properties that guarantee reliable database transactions:

- **Atomicity**: All or nothing operations
- **Consistency**: Data remains in a valid state
- **Isolation**: Transactions don't interfere with each other
- **Durability**: Changes are permanent after commit

MongoDB provides ACID compliance within a single document and across documents in multi-document transactions (since v4.0+).

## What is a Document Store?

A document store is a type of NoSQL database where data is stored in flexible, JSON-like documents.

Example:
```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "orders": [
    { "id": 1, "product": "Book", "qty": 2 }
  ]
}
```

MongoDB is a popular document-oriented database.

## Types of NoSQL Databases

| Type          | Description                        | Examples           |
| ------------- | ---------------------------------- | ------------------ |
| Document      | Stores structured JSON-like data   | MongoDB, Couchbase |
| Key-Value     | Simple key-value pairs             | Redis, DynamoDB    |
| Column-family | Columns stored separately by group | Cassandra, HBase   |
| Graph         | Nodes and edges for relationships  | Neo4j, ArangoDB    |

## Benefits of NoSQL Databases

* Flexible and dynamic schema
* High scalability via horizontal scaling
* High performance for read/write-heavy applications
* Well-suited for semi-structured or unstructured data
* Ideal for agile and rapidly changing environments

## Querying MongoDB

Basic queries using MongoDB Query Language (MQL):

* Find a user:

  ```js
  db.users.findOne({ name: "Alice" })
  ```

* Find users older than 30:

  ```js
  db.users.find({ age: { $gt: 30 } })
  ```

## Insert, Update, Delete in MongoDB

* Insert:

  ```js
  db.users.insertOne({ name: "Bob", age: 28 })
  ```

* Update:

  ```js
  db.users.updateOne({ name: "Bob" }, { $set: { age: 29 } })
  ```

* Delete:

  ```js
  db.users.deleteOne({ name: "Bob" })
  ```

## Using MongoDB in Applications

### Python with MongoEngine

Install:

```bash
pip install mongoengine
```

Example:

```python
import mongoengine

mongoengine.connect(db="my_db", alias="core")

class User(mongoengine.Document):
    name = mongoengine.StringField()
    age = mongoengine.IntField()
    meta = {'db_alias': 'core'}

User(name="Alice", age=30).save()
```

### Node.js with Mongoose

Install:

```bash
npm install mongoose
```

Example:

```js
const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/my_db');

const User = mongoose.model('User', {
  name: String,
  age: Number
});

new User({ name: 'Alice', age: 30 }).save();
```
