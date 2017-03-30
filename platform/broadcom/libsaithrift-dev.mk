# libsaithrift-dev package

LIBSAITHRIFT_DEV_BRCM = libsaithrift-dev_0.9.4_amd64.deb
$(LIBSAITHRIFT_DEV_BRCM)_SRC_PATH = $(SRC_PATH)/SAI
$(LIBSAITHRIFT_DEV_BRCM)_DEPENDS += $(LIBTHRIFT) $(LIBTHRIFT_DEV) $(THRIFT_COMPILER) $(BRCM_SAI) $(BRCM_SAI_DEV)
$(LIBSAITHRIFT_DEV_BRCM)_RDEPENDS += $(LIBTHRIFT) $(BRCM_SAI)
SONIC_DPKG_DEBS += $(LIBSAITHRIFT_DEV_BRCM)