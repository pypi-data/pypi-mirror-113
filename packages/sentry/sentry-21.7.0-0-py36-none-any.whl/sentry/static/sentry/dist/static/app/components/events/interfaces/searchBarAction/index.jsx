Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function SearchBarAction(_a) {
    var onChange = _a.onChange, query = _a.query, placeholder = _a.placeholder, filter = _a.filter, className = _a.className;
    return (<Wrapper className={className}>
      {filter}
      <StyledSearchBar onChange={onChange} query={query} placeholder={placeholder} blendWithFilter={!!filter}/>
    </Wrapper>);
}
exports.default = SearchBarAction;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  width: 100%;\n  margin-top: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    grid-gap: 0;\n    grid-template-columns: ", ";\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    width: 400px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  width: 100%;\n  margin-top: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    grid-gap: 0;\n    grid-template-columns: ", ";\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    width: 400px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), space_1.default(2), space_1.default(1), function (props) { return props.theme.breakpoints[0]; }, function (p) {
    return p.children && react_1.Children.toArray(p.children).length === 1
        ? '1fr'
        : 'max-content 1fr';
}, function (props) { return props.theme.breakpoints[1]; }, function (props) { return props.theme.breakpoints[3]; });
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"], ["\n  width: 100%;\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"])), function (props) { return props.theme.breakpoints[0]; }, function (p) {
    return p.blendWithFilter &&
        "\n        .search-input,\n        .search-input:focus {\n          border-top-left-radius: 0;\n          border-bottom-left-radius: 0;\n        }\n      ";
});
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map