Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var search_1 = tslib_1.__importDefault(require("app/components/search"));
var searchResult_1 = tslib_1.__importDefault(require("app/components/search/searchResult"));
var searchResultWrapper_1 = tslib_1.__importDefault(require("app/components/search/searchResultWrapper"));
var helpSource_1 = tslib_1.__importDefault(require("app/components/search/sources/helpSource"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var renderResult = function (_a) {
    var _b;
    var item = _a.item, matches = _a.matches, itemProps = _a.itemProps, highlighted = _a.highlighted;
    var sectionHeading = item.sectionHeading !== undefined ? (<SectionHeading>
        <icons_1.IconWindow />
        {locale_1.t('From %s', item.sectionHeading)}
        <Count>{locale_1.tn('%s result', '%s results', (_b = item.sectionCount) !== null && _b !== void 0 ? _b : 0)}</Count>
      </SectionHeading>) : null;
    if (item.empty) {
        return (<React.Fragment>
        {sectionHeading}
        <Empty>{locale_1.t('No results from %s', item.sectionHeading)}</Empty>
      </React.Fragment>);
    }
    return (<React.Fragment>
      {sectionHeading}
      <searchResultWrapper_1.default {...itemProps} highlighted={highlighted}>
        <searchResult_1.default highlighted={highlighted} item={item} matches={matches}/>
      </searchResultWrapper_1.default>
    </React.Fragment>);
};
// TODO(ts): Type based on Search props once that has types
var HelpSearch = function (props) { return (<search_1.default {...props} sources={[helpSource_1.default]} minSearch={3} closeOnSelect={false} renderItem={renderResult}/>); };
var SectionHeading = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  background: ", ";\n  padding: ", " ", ";\n\n  &:not(:first-of-type) {\n    border-top: 1px solid ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  background: ", ";\n  padding: ", " ", ";\n\n  &:not(:first-of-type) {\n    border-top: 1px solid ", ";\n  }\n"])), space_1.default(1), function (p) { return p.theme.backgroundSecondary; }, space_1.default(1), space_1.default(2), function (p) { return p.theme.innerBorder; });
var Count = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var Empty = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  color: ", ";\n  font-size: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  color: ", ";\n  font-size: ", ";\n  border-top: 1px solid ", ";\n"])), space_1.default(2), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.innerBorder; });
exports.default = HelpSearch;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=helpSearch.jsx.map