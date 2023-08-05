Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var confirmHeader_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/confirmHeader"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
/**
 * List u2f devices w/ ability to remove a single device
 */
function U2fEnrolledDetails(_a) {
    var className = _a.className, isEnrolled = _a.isEnrolled, devices = _a.devices, id = _a.id, onRemoveU2fDevice = _a.onRemoveU2fDevice;
    if (id !== 'u2f' || !isEnrolled) {
        return null;
    }
    var hasDevices = devices === null || devices === void 0 ? void 0 : devices.length;
    // Note Tooltip doesn't work because of bootstrap(?) pointer events for disabled buttons
    var isLastDevice = hasDevices === 1;
    return (<panels_1.Panel className={className}>
      <panels_1.PanelHeader>{locale_1.t('Device name')}</panels_1.PanelHeader>

      <panels_1.PanelBody>
        {!hasDevices && (<emptyMessage_1.default>{locale_1.t('You have not added any U2F devices')}</emptyMessage_1.default>)}
        {hasDevices &&
            (devices === null || devices === void 0 ? void 0 : devices.map(function (device) { return (<DevicePanelItem key={device.name}>
              <DeviceInformation>
                <Name>{device.name}</Name>
                <FadedDateTime date={device.timestamp}/>
              </DeviceInformation>

              <Actions>
                <confirm_1.default onConfirm={function () { return onRemoveU2fDevice(device); }} disabled={isLastDevice} message={<react_1.Fragment>
                      <confirmHeader_1.default>
                        {locale_1.t('Do you want to remove U2F device?')}
                      </confirmHeader_1.default>
                      <textBlock_1.default>
                        {locale_1.t("Are you sure you want to remove the U2F device \"" + device.name + "\"?")}
                      </textBlock_1.default>
                    </react_1.Fragment>}>
                  <button_1.default size="small" priority="danger">
                    <tooltip_1.default disabled={!isLastDevice} title={locale_1.t('Can not remove last U2F device')}>
                      <icons_1.IconDelete size="xs"/>
                    </tooltip_1.default>
                  </button_1.default>
                </confirm_1.default>
              </Actions>
            </DevicePanelItem>); }))}
        <AddAnotherPanelItem>
          <button_1.default type="button" to="/settings/account/security/mfa/u2f/enroll/" size="small">
            {locale_1.t('Add Another Device')}
          </button_1.default>
        </AddAnotherPanelItem>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
var DevicePanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var DeviceInformation = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex: 1;\n\n  padding: ", ";\n  padding-right: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  flex: 1;\n\n  padding: ", ";\n  padding-right: 0;\n"])), space_1.default(2));
var FadedDateTime = styled_1.default(dateTime_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  opacity: 0.6;\n"], ["\n  font-size: ", ";\n  opacity: 0.6;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var Name = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Actions = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space_1.default(2));
var AddAnotherPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n  padding: ", ";\n"], ["\n  justify-content: flex-end;\n  padding: ", ";\n"])), space_1.default(2));
exports.default = styled_1.default(U2fEnrolledDetails)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(4));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=u2fEnrolledDetails.jsx.map