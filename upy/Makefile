
UPYTHON_VER	= 1.11
UPYTHON		= micropython-$(UPYTHON_VER)
UPYTHON_GZ	= $(UPYTHON).tar.xz

CWD	 = $(CURDIR)
GZ  ?= $(HOME)/gz

MAKE := $(MAKE) -j$(shell grep proc /proc/cpuinfo|wc -l)

PORTS = $(UPYTHON)/ports/unix

build: $(CWD)/micropython
	$< -m upip install picoweb

$(CWD)/micropython: $(PORTS)/micropython
	cp $< $@

$(PORTS)/micropython: $(UPYTHON)/README.md
	cd $(PORTS) ; $(MAKE) $(MODS) clean
	cd $(PORTS) ; $(MAKE) $(MODS) deplibs
	cd $(PORTS) ; $(MAKE) $(MODS) 

$(UPYTHON)/README.md: $(GZ)/$(UPYTHON_GZ)
	xzcat $< | tar x && touch $@

$(GZ)/$(UPYTHON_GZ):
	wget -c -O $@ http://micropython.org/resources/source/$(UPYTHON_GZ)
