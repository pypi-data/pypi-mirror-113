from conductor.airfinder.devices.nordic_access_point import NordicAccessPoint, NordicAPMessageSpecV2_0_5
from conductor.util import Version


class XLEAccessPoint(NordicAccessPoint):

    application = "0fd6d1a99148c4534548"

    @property
    def bootloader_version(self):
        """ Message Spec Version of the AP """
        major = self._md.get('bootloaderVersionMajor')
        minor = self._md.get('bootloaderVersionMinor')
        tag = self._md.get('bootloaderVersionTag')
        if not major or not minor or not tag:
            return None
        return Version(int(major), int(minor), int(tag))

    @classmethod
    def _get_spec(cls, vers):
        # TODO: Implement XLE msg spec.
        return NordicAPMessageSpecV2_0_5()
