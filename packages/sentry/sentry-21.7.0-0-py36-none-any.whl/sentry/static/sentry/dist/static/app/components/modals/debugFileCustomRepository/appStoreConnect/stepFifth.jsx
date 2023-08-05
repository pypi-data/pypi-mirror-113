Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
function StepFifth(_a) {
    var _b, _c;
    var appleStoreOrgs = _a.appleStoreOrgs, stepFifthData = _a.stepFifthData, onSetStepFifthData = _a.onSetStepFifthData;
    return (<StyledSelectField name="organization" label={locale_1.t('iTunes Organization')} choices={appleStoreOrgs.map(function (appleStoreOrg) { return [
            appleStoreOrg.organizationId,
            appleStoreOrg.name,
        ]; })} placeholder={locale_1.t('Select organization')} onChange={function (organizationId) {
            var selectedAppleStoreOrg = appleStoreOrgs.find(function (appleStoreOrg) { return appleStoreOrg.organizationId === organizationId; });
            onSetStepFifthData({ org: selectedAppleStoreOrg });
        }} value={(_c = (_b = stepFifthData.org) === null || _b === void 0 ? void 0 : _b.organizationId) !== null && _c !== void 0 ? _c : ''} inline={false} flexibleControlStateSize stacked required/>);
}
exports.default = StepFifth;
var StyledSelectField = styled_1.default(selectField_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=stepFifth.jsx.map