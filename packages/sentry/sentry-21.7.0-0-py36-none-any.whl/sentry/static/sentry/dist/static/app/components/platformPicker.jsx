Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_keydown_1 = tslib_1.__importDefault(require("react-keydown"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var platformicons_1 = require("platformicons");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var listLink_1 = tslib_1.__importDefault(require("app/components/links/listLink"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var platformCategories_1 = tslib_1.__importStar(require("app/data/platformCategories"));
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var PLATFORM_CATEGORIES = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(platformCategories_1.default)), [{ id: 'all', name: locale_1.t('All') }]);
var PlatformList = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 112px);\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 112px);\n  margin-bottom: ", ";\n"])), space_1.default(1), space_1.default(2));
var PlatformPicker = /** @class */ (function (_super) {
    tslib_1.__extends(PlatformPicker, _super);
    function PlatformPicker() {
        var _a;
        var _this = _super.apply(this, tslib_1.__spreadArray([], tslib_1.__read(arguments))) || this;
        _this.state = {
            category: (_a = _this.props.defaultCategory) !== null && _a !== void 0 ? _a : PLATFORM_CATEGORIES[0].id,
            filter: _this.props.noAutoFilter ? '' : (_this.props.platform || '').split('-')[0],
        };
        _this.logSearch = debounce_1.default(function () {
            var _a;
            if (_this.state.filter) {
                advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.platformpicker_search', {
                    search: _this.state.filter.toLowerCase(),
                    num_results: _this.platformList.length,
                    source: _this.props.source,
                }, (_a = _this.props.organization) !== null && _a !== void 0 ? _a : null);
            }
        }, 300);
        _this.searchInput = React.createRef();
        return _this;
    }
    Object.defineProperty(PlatformPicker.prototype, "platformList", {
        get: function () {
            var category = this.state.category;
            var currentCategory = platformCategories_1.default.find(function (_a) {
                var id = _a.id;
                return id === category;
            });
            var filter = this.state.filter.toLowerCase();
            var subsetMatch = function (platform) {
                var _a;
                return platform.id.includes(filter) ||
                    platform.name.toLowerCase().includes(filter) ||
                    ((_a = platformCategories_1.filterAliases[platform.id]) === null || _a === void 0 ? void 0 : _a.some(function (alias) { return alias.includes(filter); }));
            };
            var categoryMatch = function (platform) {
                var _a;
                return category === 'all' ||
                    ((_a = currentCategory === null || currentCategory === void 0 ? void 0 : currentCategory.platforms) === null || _a === void 0 ? void 0 : _a.includes(platform.id));
            };
            var filtered = platforms_1.default
                .filter(this.state.filter ? subsetMatch : categoryMatch)
                .sort(function (a, b) { return a.id.localeCompare(b.id); });
            return this.props.showOther ? filtered : filtered.filter(function (_a) {
                var id = _a.id;
                return id !== 'other';
            });
        },
        enumerable: false,
        configurable: true
    });
    PlatformPicker.prototype.focusSearch = function (e) {
        var _a, _b;
        if (e.target !== this.searchInput.current) {
            (_b = (_a = this.searchInput) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.focus();
            e.preventDefault();
        }
    };
    PlatformPicker.prototype.render = function () {
        var _this = this;
        var platformList = this.platformList;
        var _a = this.props, setPlatform = _a.setPlatform, listProps = _a.listProps, listClassName = _a.listClassName;
        var _b = this.state, filter = _b.filter, category = _b.category;
        return (<React.Fragment>
        <NavContainer>
          <CategoryNav>
            {PLATFORM_CATEGORIES.map(function (_a) {
                var id = _a.id, name = _a.name;
                return (<listLink_1.default key={id} onClick={function (e) {
                        var _a;
                        advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.platformpicker_category', { category: id, source: _this.props.source }, (_a = _this.props.organization) !== null && _a !== void 0 ? _a : null);
                        _this.setState({ category: id, filter: '' });
                        e.preventDefault();
                    }} to="" isActive={function () { return id === (filter ? 'all' : category); }}>
                {name}
              </listLink_1.default>);
            })}
          </CategoryNav>
          <SearchBar>
            <icons_1.IconSearch size="xs"/>
            <input type="text" ref={this.searchInput} value={filter} placeholder={locale_1.t('Filter Platforms')} onChange={function (e) { return _this.setState({ filter: e.target.value }, _this.logSearch); }}/>
          </SearchBar>
        </NavContainer>
        <PlatformList className={listClassName} {...listProps}>
          {platformList.map(function (platform) { return (<PlatformCard data-test-id={"platform-" + platform.id} key={platform.id} platform={platform} selected={_this.props.platform === platform.id} onClear={function (e) {
                    setPlatform(null);
                    e.stopPropagation();
                }} onClick={function () {
                    var _a;
                    advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.select_platform', {
                        platform_id: platform.id,
                        source: _this.props.source,
                    }, (_a = _this.props.organization) !== null && _a !== void 0 ? _a : null);
                    setPlatform(platform.id);
                }}/>); })}
        </PlatformList>
        {platformList.length === 0 && (<emptyMessage_1.default icon={<icons_1.IconProject size="xl"/>} title={locale_1.t("We don't have an SDK for that yet!")}>
            {locale_1.tct("Not finding your platform? You can still create your project,\n              but looks like we don't have an official SDK for your platform\n              yet. However, there's a rich ecosystem of community supported\n              SDKs (including Perl, CFML, Clojure, and ActionScript). Try\n              [search:searching for Sentry clients] or contacting support.", {
                    search: (<externalLink_1.default href="https://github.com/search?q=-org%3Agetsentry+topic%3Asentry&type=Repositories"/>),
                })}
          </emptyMessage_1.default>)}
      </React.Fragment>);
    };
    PlatformPicker.defaultProps = {
        showOther: true,
    };
    tslib_1.__decorate([
        react_keydown_1.default('/')
    ], PlatformPicker.prototype, "focusSearch", null);
    return PlatformPicker;
}(React.Component));
var NavContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr minmax(0, 300px);\n  align-items: start;\n  border-bottom: 1px solid ", ";\n"], ["\n  margin-bottom: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr minmax(0, 300px);\n  align-items: start;\n  border-bottom: 1px solid ", ";\n"])), space_1.default(2), space_1.default(2), function (p) { return p.theme.border; });
var SearchBar = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  padding: 0 8px;\n  color: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 15px;\n  margin-top: -", ";\n\n  input {\n    border: none;\n    background: none;\n    padding: 2px 4px;\n    width: 100%;\n    /* Ensure a consistent line height to keep the input the desired height */\n    line-height: 24px;\n\n    &:focus {\n      outline: none;\n    }\n  }\n"], ["\n  ", ";\n  padding: 0 8px;\n  color: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 15px;\n  margin-top: -", ";\n\n  input {\n    border: none;\n    background: none;\n    padding: 2px 4px;\n    width: 100%;\n    /* Ensure a consistent line height to keep the input the desired height */\n    line-height: 24px;\n\n    &:focus {\n      outline: none;\n    }\n  }\n"])), function (p) { return input_1.inputStyles(p); }, function (p) { return p.theme.subText; }, space_1.default(0.75));
var CategoryNav = styled_1.default(navTabs_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  margin-top: 4px;\n  white-space: nowrap;\n\n  > li {\n    float: none;\n    display: inline-block;\n  }\n"], ["\n  margin: 0;\n  margin-top: 4px;\n  white-space: nowrap;\n\n  > li {\n    float: none;\n    display: inline-block;\n  }\n"])));
var StyledPlatformIcon = styled_1.default(platformicons_1.PlatformIcon)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space_1.default(2));
var ClearButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: -6px;\n  right: -6px;\n  height: 22px;\n  width: 22px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: 50%;\n  background: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  top: -6px;\n  right: -6px;\n  height: 22px;\n  width: 22px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: 50%;\n  background: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.textColor; });
ClearButton.defaultProps = {
    icon: <icons_1.IconClose isCircled size="xs"/>,
    borderless: true,
    size: 'xsmall',
};
var PlatformCard = styled_1.default(function (_a) {
    var platform = _a.platform, selected = _a.selected, onClear = _a.onClear, props = tslib_1.__rest(_a, ["platform", "selected", "onClear"]);
    return (<div {...props}>
    <StyledPlatformIcon platform={platform.id} size={56} radius={5} withLanguageIcon format="lg"/>

    <h3>{platform.name}</h3>
    {selected && <ClearButton onClick={onClear}/>}
  </div>);
})(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  padding: 0 0 14px;\n  border-radius: 4px;\n  cursor: pointer;\n  background: ", ";\n\n  &:hover {\n    background: ", ";\n  }\n\n  h3 {\n    flex-grow: 1;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 100%;\n    color: ", ";\n    text-align: center;\n    font-size: ", ";\n    text-transform: uppercase;\n    margin: 0;\n    padding: 0 ", ";\n    line-height: 1.2;\n  }\n"], ["\n  position: relative;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  padding: 0 0 14px;\n  border-radius: 4px;\n  cursor: pointer;\n  background: ", ";\n\n  &:hover {\n    background: ", ";\n  }\n\n  h3 {\n    flex-grow: 1;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 100%;\n    color: ", ";\n    text-align: center;\n    font-size: ", ";\n    text-transform: uppercase;\n    margin: 0;\n    padding: 0 ", ";\n    line-height: 1.2;\n  }\n"])), function (p) { return p.selected && p.theme.alert.info.backgroundLight; }, function (p) { return p.theme.alert.muted.backgroundLight; }, function (p) { return (p.selected ? p.theme.textColor : p.theme.subText); }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(0.5));
exports.default = PlatformPicker;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=platformPicker.jsx.map