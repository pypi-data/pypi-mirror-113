Object.defineProperty(exports, "__esModule", { value: true });
exports.TagAndMessageWrapper = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function UnhandledTag() {
    return (<TagWrapper>
      <tooltip_1.default title={locale_1.t('An unhandled error was detected in this Issue.')}>
        <tag_1.default type="error">{locale_1.t('Unhandled')}</tag_1.default>
      </tooltip_1.default>
    </TagWrapper>);
}
var TagWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var TagAndMessageWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
exports.TagAndMessageWrapper = TagAndMessageWrapper;
exports.default = UnhandledTag;
var templateObject_1, templateObject_2;
//# sourceMappingURL=unhandledTag.jsx.map