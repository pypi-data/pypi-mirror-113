Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
function StepTwo(_a) {
    var _b, _c;
    var stepTwoData = _a.stepTwoData, onSetStepTwoData = _a.onSetStepTwoData, appStoreApps = _a.appStoreApps;
    return (<StyledSelectField name="application" label={locale_1.t('App Store Connect application')} choices={appStoreApps.map(function (appStoreApp) { return [appStoreApp.appId, appStoreApp.name]; })} placeholder={locale_1.t('Select application')} onChange={function (appId) {
            var selectedAppStoreApp = appStoreApps.find(function (appStoreApp) { return appStoreApp.appId === appId; });
            onSetStepTwoData({ app: selectedAppStoreApp });
        }} value={(_c = (_b = stepTwoData.app) === null || _b === void 0 ? void 0 : _b.appId) !== null && _c !== void 0 ? _c : ''} inline={false} flexibleControlStateSize stacked required/>);
}
exports.default = StepTwo;
var StyledSelectField = styled_1.default(selectField_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=stepTwo.jsx.map