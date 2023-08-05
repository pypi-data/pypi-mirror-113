Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var events_1 = require("app/utils/events");
var Header = function (_a) {
    var traceID = _a.traceID;
    return (<Wrapper>
    <h4>{locale_1.t('Issues with the same trace ID')}</h4>
    {traceID ? (<clipboard_1.default value={traceID}>
        <ClipboardWrapper>
          <span>{events_1.getShortEventId(traceID)}</span>
          <icons_1.IconCopy />
        </ClipboardWrapper>
      </clipboard_1.default>) : (<span>{'-'}</span>)}
  </Wrapper>);
};
exports.default = Header;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  h4 {\n    font-size: ", ";\n    color: ", ";\n    font-weight: normal;\n    margin-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  h4 {\n    font-size: ", ";\n    color: ", ";\n    font-weight: normal;\n    margin-bottom: 0;\n  }\n"])), space_1.default(1), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; });
var ClipboardWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  &:hover {\n    cursor: pointer;\n  }\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=header.jsx.map