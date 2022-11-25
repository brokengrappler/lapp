
# LAPP MVP

Using AWS to serve youth swim meet results.


1) Serve POST API in AWS to upload
   1) swimmer id and info
   2) swimmer parent information
   3) swim club
   4) swim meet information
      1) swim meet results
2) Lambda posts data above to RDS
3) Result POST -> SQS -> SNS ->
   1) lambda to RDS
   2) lambda to SNS for results

