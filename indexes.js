db = connect("localhost:81/meteor");
db.summaries.createIndex({source: 1}, {background: true});
db.summaries.createIndex({date: 1}, {background: true});
db.sources.createIndex({name: 1}, {background: true, unique: true});
db.sources.createIndex({type: 1}, {background: true});
db.sources.createIndex({topics: 1}, {background: true});


