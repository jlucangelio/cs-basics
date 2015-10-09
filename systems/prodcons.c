#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static const size_t kCapacity = 10;
static const unsigned int kNumCycles = 100;

static const useconds_t kProdDelay = 1000;
static const useconds_t kConsDelay = 1000;

pthread_mutex_t mutex;
pthread_cond_t not_full_cv;
pthread_cond_t not_empty_cv;

int values[kCapacity];
size_t first_available_idx = 0;

void* produce(void* ptid) {
  unsigned int i;
  long tid = (long)ptid;
  printf("produce %ld\n", tid);

  for (i = 0; i < kNumCycles; i++) {
    pthread_mutex_lock(&mutex);
    if (first_available_idx == kCapacity) {
      /* No more space available in the shared buffer,
       * wait until the buffer is not full anymore.
       */
      printf("producer: wait(not_full)\n");
      pthread_cond_wait(&not_full_cv, &mutex);
    }
    values[first_available_idx] = i;
    printf("producer: cycle %u, index %lu, value %d\n", i, first_available_idx,
           values[first_available_idx]);
    ++first_available_idx;
    if (first_available_idx == 1) {
      /* Produced the first element in the shared buffer,
       * signal that the buffer is not empty anymore.
       */
      printf("producer: signal(not_empty)\n");
      pthread_cond_signal(&not_empty_cv);
    }
    pthread_mutex_unlock(&mutex);
    usleep(kProdDelay);
  }
  pthread_exit(NULL);
}

void* consume(void* ctid) {
  long tid = (long)ctid;
  printf("consumer %ld\n", tid);

  for (unsigned int i = 0; i < kNumCycles; i++) {
    pthread_mutex_lock(&mutex);
    if (first_available_idx == 0) {
      /* No elements available in the shared buffer,
       * wait until the buffer is not empty anymore.
       */
      printf("consumer: wait(not_empty)\n");
      pthread_cond_wait(&not_empty_cv, &mutex);
    }
    --first_available_idx;
    printf("consumer cycle %u, index %lu, value %d\n", i, first_available_idx,
           values[first_available_idx]);
    if (first_available_idx == kCapacity - 1) {
      /* Consumed the last element in the shared buffer,
       * signal that the buffer is not full anymore.
       */
      printf("consumer: signal(not_full)\n");
      pthread_cond_signal(&not_full_cv);
    }
    pthread_mutex_unlock(&mutex);
    usleep(kConsDelay);
  }
  pthread_exit(NULL);
}

int main(int argc, char* argv[]) {
  pthread_t workers[2];
  pthread_attr_t attr;

  /* Initialize mutex and condition variable objects. */
  pthread_mutex_init(&mutex, NULL);
  pthread_cond_init(&not_full_cv, NULL);
  pthread_cond_init(&not_empty_cv, NULL);

  long ptid = 0;
  long ctid = 1;

  pthread_attr_init(&attr);
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

  pthread_create(&workers[0], NULL, produce, (void*)ptid);
  pthread_create(&workers[1], NULL, consume, (void*)ctid);

  pthread_join(workers[0], NULL);
  pthread_join(workers[1], NULL);

  /* Clean up and exit. */
  pthread_mutex_destroy(&mutex);
  pthread_cond_destroy(&not_full_cv);
  pthread_cond_destroy(&not_empty_cv);
  pthread_exit(NULL);
}
