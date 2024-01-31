# 🐇 Parallelization

### Tutorial on Parallelization in R with \`mclapply\`



When you have a list of repetitive tasks, you may be able to speed it up by adding more computing power. If each task is completely independent of the others, then it is a prime candidate for executing those tasks in parallel, each on its own core\


#### Step 1: Loading Necessary Libraries

The \`parallel\` library can be used to send tasks (encoded as function calls) to each of the processing cores on your machine in parallel. This is done by using the \`parallel::mclapply\` function, which is analogous to \`lapply\`, but distributes the tasks to multiple processors. \`mclapply\` gathers up the responses from each of these function calls, and returns a list of responses that is the same length as the list or vector of input data (one return per input item).

`R`\
`# Install and load the 'parallel' library`\
`install.packages("parallel")`\
`library(parallel)`



#### Step 2: Define the Processing Function

The essence of parallelization is to execute a \*\*function\*\* simultaneously on different data (a list of data). The first step is to define the function to be executed. For example, let's create a simple function that takes a number as input and returns its square.

&#x20;

`R`\
`# Define the processing function`\
`process_number <- function(num) {`\
&#x20; `result <- num^2`\
&#x20; `return(result)`\
`}`



#### Step 3: Create a List of Numbers

The essence of parallelization is to execute a function simultaneously on different data (\*\*a list of data\*\*). Therefore, it is crucial to create a list containing all the elements on which the function will be applied. For example, let's create a list of numbers on which we want to apply the function in parallel..

`R`\
`numbers_list <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)`



#### Step 4: Parallelize Processing with \`mclapply\`

To parallelize the function on each element of the list, \`mclapply\` is employed.

`R`\
`mclapply(X, FUN, ..., mc.cores = detectCores())`\


&#x20;

* _**X**_: a vector (atomic or list) or an expressions vector. Other objects (including classed objects) will be coerced by \`as.list\`.
* _**FUN**_: the function to be applied to (\`mclapply\`) each element of \`X\`.

&#x20;

Define the number of cores to be used for parallelization (in this example, all available cores). _**FUN**_ should be written in this form:

`R`\
`#FUN`\
`function(y) function_name(y,arg2,arg3, ...)`

&#x20;

* _**y**_ represents each element of \`X\` (can be any name).
* _**function\_name**_\*\* is the name of the function to apply to each element of \`X\`.

&#x20;

Here's an example of using \`mclapply\`:\
`R`\
`# Parallelize processing with mclapply`\
`processing <- mclapply(`\
&#x20; `numbers_list,`\
&#x20; `function(num) process_number(num),`\
&#x20; `mc.cores = detectCores()`\
`)`

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&#x20;

For more information on \`mclapply\`:\
\- [https://www.rdocumentation.org/packages/parallel/versions/3.4.0/topics/mclapply](https://www.rdocumentation.org/packages/parallel/versions/3.4.0/topics/mclapply)\
\- [https://nceas.github.io/oss-lessons/parallel-computing-in-r/parallel-computing-in-r.html](https://nceas.github.io/oss-lessons/parallel-computing-in-r/parallel-computing-in-r.html)
