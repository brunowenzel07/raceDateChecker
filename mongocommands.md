db.getCollection('races').find({'racedate': '20100101'}).count()
//new date format
db.getCollection('races').find({'racedate': {$gte:new ISODate("2011-09-01T23:59:59Z"),$lte:new ISODate("2011-12-31T23:59:59Z")},})


//get no races between 2 dates
db.getCollection('races').aggregate({ $match: {
    $and: [
        { racedate: { $gte:new ISODate("2010-09-01T23:59:59Z") } },
        { racedate: { $lte:new ISODate("2011-07-01T23:59:59Z") } }
    ]
} },
{ $group: { _id : null, sum : { $sum: "$noraces" } } });


db.getCollection('races').find({}).sort( { racedate: 1 } )


# duplicate races

db.getCollection('races').aggregate([
  { $group: {
    _id: { racedate: "$racedate" },   // replace `name` here twice
    uniqueIds: { $addToSet: "$_id" },
    count: { $sum: 1 }
  } },
  { $match: {
    count: { $gte: 2 }
  } },
  { $sort : { count : -1} },
  { $limit : 10 }
]);
