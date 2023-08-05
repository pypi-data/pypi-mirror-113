Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var controlState_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/controlState"));
var types_1 = require("../../types");
var EventIdFieldStatusIcon = function (_a) {
    var status = _a.status, onClickIconClose = _a.onClickIconClose;
    switch (status) {
        case types_1.EventIdStatus.ERROR:
        case types_1.EventIdStatus.INVALID:
        case types_1.EventIdStatus.NOT_FOUND:
            return (<CloseIcon onClick={onClickIconClose}>
          <tooltip_1.default title={locale_1.t('Clear event ID')}>
            <StyledIconClose size="xs"/>
          </tooltip_1.default>
        </CloseIcon>);
        case types_1.EventIdStatus.LOADING:
            return <controlState_1.default isSaving/>;
        case types_1.EventIdStatus.LOADED:
            return <icons_1.IconCheckmark color="green300"/>;
        default:
            return null;
    }
};
exports.default = EventIdFieldStatusIcon;
var CloseIcon = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  :first-child {\n    line-height: 0;\n  }\n"], ["\n  :first-child {\n    line-height: 0;\n  }\n"])));
var StyledIconClose = styled_1.default(icons_1.IconClose)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n  cursor: pointer;\n"], ["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n  cursor: pointer;\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=eventIdFieldStatusIcon.jsx.map