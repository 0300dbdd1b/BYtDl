# Variables
SRCDIR      = ./src/
INCDIR      = ./src/includes/
SRCNAME     = main.cpp \
			  YtDownloader.cpp\

SRCS        = $(addprefix $(SRCDIR), $(SRCNAME))
OBJS        = $(SRCS:.cpp=.o)
CC          = g++
CFLAGS      = -std=c++17 -Wall -Wextra -g3
FTXUI_DIR  = ./extern/ftxtui
FTXUI_SRC  = $(FTXUI_DIR)
CXXFLAGS    = $(CFLAGS) -I $(INCDIR) -I $(FTXUI_SRC)/include/
NAME        = BYtDl

# Detect OS
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S), Darwin)
    LDFLAGS += -L $(FTXUI_SRC)/build -lcurl -lftxui-component -lftxui-dom -lftxui-screen
else ifeq ($(OS), Windows_NT)
    LDFLAGS += -L $(FTXUI_SRC)/build -lcurl -lftxui-component -lftxui-dom -lftxui-screen
else
    LDFLAGS += -L $(FTXUI_SRC)/build -lcurl -lftxui-component -lftxui-dom -lftxui-screen
endif

# Targets
all: $(NAME) ## Build the project

ftxui: ## Download and compile raylib if not already done
	@if [ ! -d "$(FTXUI_DIR)" ]; then \
		echo "Cloning FTXUI..."; \
		git clone --depth 1 https://github.com/ArthurSonzogni/FTXUI.git $(FTXUI_DIR); \
	fi
	@if [ ! -f "$(FTXUI_SRC)/libftxui-component.a" ]; then \
		echo "Compiling FTXUI..."; \
		mkdir build && cd build;	\
		cmake ..;					\
		make;						\
	fi

rebuild_ftxui: ## Clean and recompile raylib
	@if [ -d "$(FTXUI_DIR)" ]; then \
		echo "Recompiling FTXUI..."; \
		cd $(FTXUI_SRC) && make clean && make; \
	else \
		$(MAKE) ftxui; \
	fi

$(NAME): $(OBJS)
	$(CC) $(OBJS) $(CXXFLAGS) $(LDFLAGS) -o $(NAME)

$(SRCDIR)%.o: $(SRCDIR)%.cpp
	$(CC) $(CXXFLAGS) -c $< -o $@

clean: ## Remove all object files
	rm -f $(OBJS)

fclean: clean ## Remove all object files and the executable
	rm -f $(NAME)

re: fclean all ## Rebuild the project

x: all clean

help: ## List all commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
