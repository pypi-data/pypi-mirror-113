Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var UnhandledTag = function () { return (<tooltip_1.default title={locale_1.t('An unhandled error was detected in this Issue.')}>
    <UnhandledTagWrapper>
      <StyledIconFire size="xs" color="red300"/>
      {locale_1.t('Unhandled')}
    </UnhandledTagWrapper>
  </tooltip_1.default>); };
exports.default = UnhandledTag;
var UnhandledTagWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  white-space: nowrap;\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  white-space: nowrap;\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
var StyledIconFire = styled_1.default(icons_1.IconFire)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: 3px;\n"], ["\n  margin-right: 3px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=unhandledTag.jsx.map