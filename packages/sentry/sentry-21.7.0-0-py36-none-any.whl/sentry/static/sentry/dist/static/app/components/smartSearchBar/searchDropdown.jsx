Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("./types");
var SearchDropdown = /** @class */ (function (_super) {
    tslib_1.__extends(SearchDropdown, _super);
    function SearchDropdown() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderDescription = function (item) {
            var searchSubstring = _this.props.searchSubstring;
            if (!searchSubstring) {
                return item.desc;
            }
            var text = item.desc;
            if (!text) {
                return null;
            }
            var idx = text.toLowerCase().indexOf(searchSubstring.toLowerCase());
            if (idx === -1) {
                return item.desc;
            }
            return (<span>
        {text.substr(0, idx)}
        <strong>{text.substr(idx, searchSubstring.length)}</strong>
        {text.substr(idx + searchSubstring.length)}
      </span>);
        };
        _this.renderHeaderItem = function (item) { return (<SearchDropdownGroup key={item.title}>
      <SearchDropdownGroupTitle>
        {item.icon}
        {item.title && item.title}
        {item.desc && <span>{item.desc}</span>}
      </SearchDropdownGroupTitle>
    </SearchDropdownGroup>); };
        _this.renderItem = function (item) { return (<SearchListItem key={item.value || item.desc} className={item.active ? 'active' : undefined} data-test-id="search-autocomplete-item" onClick={_this.props.onClick.bind(_this, item.value, item)} ref={function (element) { var _a; return item.active && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}>
      <SearchItemTitleWrapper>
        {item.title && item.title + ' · '}
        <Description>{_this.renderDescription(item)}</Description>
      </SearchItemTitleWrapper>
    </SearchListItem>); };
        return _this;
    }
    SearchDropdown.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, loading = _a.loading, items = _a.items;
        return (<StyledSearchDropdown className={className}>
        {loading ? (<LoadingWrapper key="loading" data-test-id="search-autocomplete-loading">
            <loadingIndicator_1.default mini/>
          </LoadingWrapper>) : (<SearchItemsList>
            {items.map(function (item) {
                    var isEmpty = item.children && !item.children.length;
                    var invalidTag = item.type === types_1.ItemType.INVALID_TAG;
                    // Hide header if `item.children` is defined, an array, and is empty
                    return (<react_1.Fragment key={item.title}>
                  {invalidTag && <Info>{locale_1.t('Invalid tag')}</Info>}
                  {item.type === 'header' && _this.renderHeaderItem(item)}
                  {item.children && item.children.map(_this.renderItem)}
                  {isEmpty && !invalidTag && <Info>{locale_1.t('No items found')}</Info>}
                </react_1.Fragment>);
                })}
          </SearchItemsList>)}
      </StyledSearchDropdown>);
    };
    SearchDropdown.defaultProps = {
        searchSubstring: '',
        onClick: function () { },
    };
    return SearchDropdown;
}(react_1.PureComponent));
exports.default = SearchDropdown;
var StyledSearchDropdown = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* Container has a border that we need to account for */\n  position: absolute;\n  top: 100%;\n  left: -1px;\n  right: -1px;\n  z-index: ", ";\n  overflow: hidden;\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n"], ["\n  /* Container has a border that we need to account for */\n  position: absolute;\n  top: 100%;\n  left: -1px;\n  right: -1px;\n  z-index: ", ";\n  overflow: hidden;\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadiusBottom; });
var LoadingWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"])), space_1.default(1));
var Info = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n  font-size: ", ";\n  color: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  display: flex;\n  padding: ", " ", ";\n  font-size: ", ";\n  color: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), space_1.default(1), space_1.default(2), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.innerBorder; });
var ListItem = styled_1.default('li')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; });
var SearchDropdownGroup = styled_1.default(ListItem)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject([""], [""])));
var SearchDropdownGroupTitle = styled_1.default('header')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n\n  margin: 0;\n  padding: ", " ", ";\n\n  & > svg {\n    margin-right: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n\n  margin: 0;\n  padding: ", " ", ";\n\n  & > svg {\n    margin-right: ", ";\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(2), space_1.default(1));
var SearchItemsList = styled_1.default('ul')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n"], ["\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n"])));
var SearchListItem = styled_1.default(ListItem)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  scroll-margin: 40px 0;\n  font-size: ", ";\n  padding: ", " ", ";\n  cursor: pointer;\n\n  &:hover,\n  &.active {\n    background: ", ";\n  }\n"], ["\n  scroll-margin: 40px 0;\n  font-size: ", ";\n  padding: ", " ", ";\n  cursor: pointer;\n\n  &:hover,\n  &.active {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space_1.default(1), space_1.default(2), function (p) { return p.theme.focus; });
var SearchItemTitleWrapper = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  margin: 0;\n  line-height: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  margin: 0;\n  line-height: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.text.lineHeightHeading; }, overflowEllipsis_1.default);
var Description = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-family: ", ";\n"], ["\n  font-size: ", ";\n  font-family: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.familyMono; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=searchDropdown.jsx.map