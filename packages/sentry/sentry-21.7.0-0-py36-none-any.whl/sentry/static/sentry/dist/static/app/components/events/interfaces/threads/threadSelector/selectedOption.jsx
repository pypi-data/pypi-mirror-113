Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SelectedOption = function (_a) {
    var id = _a.id, details = _a.details;
    return (<Wrapper>
    <ThreadId>{locale_1.tct('Thread #[id]:', { id: id })}</ThreadId>
    <Label>{(details === null || details === void 0 ? void 0 : details.label) || "<" + locale_1.t('unknown') + ">"}</Label>
  </Wrapper>);
};
exports.default = SelectedOption;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: auto 1fr;\n  display: grid;\n"], ["\n  grid-template-columns: auto 1fr;\n  display: grid;\n"])));
var ThreadId = styled_1.default(textOverflow_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n  max-width: 100%;\n  text-align: left;\n"], ["\n  padding-right: ", ";\n  max-width: 100%;\n  text-align: left;\n"])), space_1.default(1));
var Label = styled_1.default(ThreadId)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.blue300; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=selectedOption.jsx.map