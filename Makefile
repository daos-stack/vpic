NAME      := vpic
SRC_EXT   := gz
TEST_PACKAGES := $(NAME) $(NAME)-impi

include packaging/Makefile_packaging.mk
