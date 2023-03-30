## Multithreaded Database Handler Feature

<b><font face="courier">keywords: interrpution, condition variable, concurrency</font></b>

Implementation of this feature is analogous to multicore CPU execution.

Each handler thread has its own ready queue, a new job request routed to a given handler thread will be pended in the queue if the thread is currently occupied by other jobs, or it will be executed instantly otherwise.

To avoid busy waiting, two types of interrpution mechanism are implemented.

1. thread will be waked up(interrupted) if the state of its ready queue changes from 'empty' to 'occupied'
2. a job execution request will be put into sleep after it is put into the ready queue, and be waked up(interrupted) by the handler thread when the results are available 



A database query execution routine is shown as follows

1. Mysql script will be wrapped into <b><font face="courier">class query</font></b> (protype in **/server/database/API.py**)

2. Job, i.e wrapped query object, wil be put into the ready queue of the handler thread specified by the parameter of  <b><font face="courier">@handler()</font></b>

3. Job waits for interruption issued when the handler thread finishes its execution
4. Results of Mysql script return