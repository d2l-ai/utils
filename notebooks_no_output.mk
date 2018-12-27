# convert all .md files into .ipynb files without evaluation.
# don't call it directly. use notebook_no_output.sh instead

# OUT_DIR = notebooks_no_output

$(OUT_DIR)/%.ipynb: $(IN_DIR)/%.md
	@mkdir -p $(@D)
	export EVAL=0; python md2ipynb.py $< $@

$(OUT_DIR)/%: $(IN_DIR)/%
	@mkdir -p $(@D)
	@cp $< $@

MARKDOWN = $(shell find $(IN_DIR) -not -path "$(IN_DIR)/build/*" -name "*.md")
IPYNB = $(patsubst $(IN_DIR)/%.md, $(OUT_DIR)/%.ipynb, $(MARKDOWN))
DEPS = $(shell find $(IN_DIR)/data -type f) $(shell find $(IN_DIR)/img -type f)
DEPS_COPIED = $(patsubst $(IN_DIR)/%, $(OUT_DIR)/%, $(DEPS))

all: $(IPYNB) $(DEPS_COPIED)
