is_le: is_le.c
	cc -o $@ $<

prodcons: prodcons.c
	cc -o $@ $< -lpthread -std=c99 -Wall -Werror

prodcons-tsan: prodcons.c
	clang -o $@ $< -lpthread -std=c99 -Wall -Werror -g -fsanitize=thread -pie -fPIC
