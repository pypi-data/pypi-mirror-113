Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledSettingsSearch = exports.SettingsSearch = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_keydown_1 = tslib_1.__importDefault(require("react-keydown"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var search_1 = tslib_1.__importDefault(require("app/components/search"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var MIN_SEARCH_LENGTH = 1;
var MAX_RESULTS = 10;
var SettingsSearch = /** @class */ (function (_super) {
    tslib_1.__extends(SettingsSearch, _super);
    function SettingsSearch() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.searchInput = React.createRef();
        return _this;
    }
    SettingsSearch.prototype.handleFocusSearch = function (e) {
        if (!this.searchInput.current) {
            return;
        }
        if (e.target === this.searchInput.current) {
            return;
        }
        e.preventDefault();
        this.searchInput.current.focus();
    };
    SettingsSearch.prototype.render = function () {
        var _this = this;
        return (<search_1.default entryPoint="settings_search" minSearch={MIN_SEARCH_LENGTH} maxResults={MAX_RESULTS} renderInput={function (_a) {
                var getInputProps = _a.getInputProps;
                return (<SearchInputWrapper>
            <SearchInputIcon size="14px"/>
            <SearchInput {...getInputProps({
                    type: 'text',
                    placeholder: locale_1.t('Search'),
                })} ref={_this.searchInput}/>
          </SearchInputWrapper>);
            }}/>);
    };
    tslib_1.__decorate([
        react_keydown_1.default('/')
    ], SettingsSearch.prototype, "handleFocusSearch", null);
    return SettingsSearch;
}(React.Component));
exports.SettingsSearch = SettingsSearch;
// This is so we can use this as a selector for emotion
var StyledSettingsSearch = styled_1.default(SettingsSearch)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
exports.StyledSettingsSearch = StyledSettingsSearch;
exports.default = StyledSettingsSearch;
var SearchInputWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var SearchInputIcon = styled_1.default(icons_1.IconSearch)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  position: absolute;\n  left: 10px;\n  top: 8px;\n"], ["\n  color: ", ";\n  position: absolute;\n  left: 10px;\n  top: 8px;\n"])), function (p) { return p.theme.gray300; });
var SearchInput = styled_1.default('input')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  background-color: ", ";\n  transition: border-color 0.15s ease;\n  font-size: 14px;\n  width: 260px;\n  line-height: 1;\n  padding: 5px 8px 4px 28px;\n  border: 1px solid ", ";\n  border-radius: 30px;\n  height: 28px;\n\n  box-shadow: inset ", ";\n\n  &:focus {\n    outline: none;\n    border: 1px solid ", ";\n  }\n\n  &::placeholder {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  background-color: ", ";\n  transition: border-color 0.15s ease;\n  font-size: 14px;\n  width: 260px;\n  line-height: 1;\n  padding: 5px 8px 4px 28px;\n  border: 1px solid ", ";\n  border-radius: 30px;\n  height: 28px;\n\n  box-shadow: inset ", ";\n\n  &:focus {\n    outline: none;\n    border: 1px solid ", ";\n  }\n\n  &::placeholder {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.formText; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; }, function (p) { return p.theme.formPlaceholder; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map