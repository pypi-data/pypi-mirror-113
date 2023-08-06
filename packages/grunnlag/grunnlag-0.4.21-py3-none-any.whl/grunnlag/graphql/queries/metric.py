from bergen.query import DelayedGQL


GET_METRIC = DelayedGQL("""
query GetMetric($id: ID!){
  metric(id: $id){
    id
    rep {
      id
    }
    key
    value
    creator {
      id
    }
    createdAt
  }
}
""")