from bergen.query import DelayedGQL


CREATE_METRIC = DelayedGQL("""
mutation CreateMetric($rep:ID!, $key: String!, $value: GenericScalar!){
  createMetric(rep: $rep, key: $key, value: $value){
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