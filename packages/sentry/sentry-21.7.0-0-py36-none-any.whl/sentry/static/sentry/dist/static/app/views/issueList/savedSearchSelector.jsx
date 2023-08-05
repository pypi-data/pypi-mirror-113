Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var dropdownControl_1 = tslib_1.__importDefault(require("app/components/dropdownControl"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var savedSearchMenu_1 = tslib_1.__importDefault(require("./savedSearchMenu"));
function SavedSearchSelector(_a) {
    var savedSearchList = _a.savedSearchList, onSavedSearchDelete = _a.onSavedSearchDelete, onSavedSearchSelect = _a.onSavedSearchSelect, organization = _a.organization, query = _a.query, sort = _a.sort;
    function getTitle() {
        var savedSearch = savedSearchList.find(function (search) { return search.query === query && search.sort === sort; });
        return savedSearch ? savedSearch.name : locale_1.t('Custom Search');
    }
    return (<dropdownControl_1.default menuWidth="35vw" blendWithActor button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
          <ButtonTitle>{getTitle()}</ButtonTitle>
        </StyledDropdownButton>);
        }}>
      <savedSearchMenu_1.default organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query} sort={sort}/>
    </dropdownControl_1.default>);
}
exports.default = SavedSearchSelector;
var StyledDropdownButton = styled_1.default(dropdownButton_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  background-color: ", ";\n  border-right: 0;\n  border-color: ", ";\n  z-index: ", ";\n  border-radius: ", ";\n  white-space: nowrap;\n  max-width: 200px;\n  margin-right: 0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border-color: ", ";\n    border-right: 0;\n  }\n"], ["\n  color: ", ";\n  background-color: ", ";\n  border-right: 0;\n  border-color: ", ";\n  z-index: ", ";\n  border-radius: ", ";\n  white-space: nowrap;\n  max-width: 200px;\n  margin-right: 0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border-color: ", ";\n    border-right: 0;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; }, function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " 0 0 0"
        : p.theme.borderRadius + " 0 0 " + p.theme.borderRadius;
}, function (p) { return p.theme.border; });
var ButtonTitle = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2;
//# sourceMappingURL=savedSearchSelector.jsx.map