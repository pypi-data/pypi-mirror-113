

from bergen.query import DelayedGQL


GET_EXPERIMENT = DelayedGQL("""
query Experiment($id: ID!){
  experiment(id: $id){
    id
    name
    description
    meta
  }
}
""")
