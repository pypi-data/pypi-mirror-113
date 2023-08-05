Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("./utils");
function SavedSearchMenuItem(_a) {
    var organization = _a.organization, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, search = _a.search, query = _a.query, sort = _a.sort, isLast = _a.isLast;
    return (<tooltip_1.default title={<react_1.Fragment>
          {search.name + " \u2022 "}
          <TooltipSearchQuery>{search.query}</TooltipSearchQuery>
          {" \u2022 "}
          {locale_1.t('Sort: ')}
          {utils_1.getSortLabel(search.sort)}
        </react_1.Fragment>} containerDisplayMode="block" delay={1000}>
      <StyledMenuItem isActive={search.query === query && search.sort === sort} isLast={isLast}>
        <MenuItemLink tabIndex={-1} onClick={function () { return onSavedSearchSelect(search); }}>
          <SearchTitle>{search.name}</SearchTitle>
          <SearchQueryContainer>
            <SearchQuery>{search.query}</SearchQuery>
            <SearchSort>
              {locale_1.t('Sort: ')}
              {utils_1.getSortLabel(search.sort)}
            </SearchSort>
          </SearchQueryContainer>
        </MenuItemLink>
        {search.isGlobal === false && search.isPinned === false && (<access_1.default organization={organization} access={['org:write']} renderNoAccessMessage={false}>
            <confirm_1.default onConfirm={function () { return onSavedSearchDelete(search); }} message={locale_1.t('Are you sure you want to delete this saved search?')} stopPropagation>
              <DeleteButton borderless title={locale_1.t('Delete this saved search')} icon={<icons_1.IconDelete />} label={locale_1.t('delete')} size="zero"/>
            </confirm_1.default>
          </access_1.default>)}
      </StyledMenuItem>
    </tooltip_1.default>);
}
function SavedSearchMenu(_a) {
    var savedSearchList = _a.savedSearchList, props = tslib_1.__rest(_a, ["savedSearchList"]);
    var savedSearches = savedSearchList.filter(function (search) { return !search.isGlobal; });
    var globalSearches = savedSearchList.filter(function (search) { return search.isGlobal; });
    // Hide "Unresolved Issues" since they have a unresolved tab
    globalSearches = globalSearches.filter(function (search) { return !search.isPinned && search.query !== 'is:unresolved'; });
    return (<react_1.Fragment>
      <MenuHeader>{locale_1.t('Saved Searches')}</MenuHeader>
      {savedSearches.length === 0 ? (<EmptyItem>{locale_1.t('No saved searches yet.')}</EmptyItem>) : (savedSearches.map(function (search, index) { return (<SavedSearchMenuItem key={search.id} search={search} isLast={index === savedSearches.length - 1} {...props}/>); }))}
      <SecondaryMenuHeader>{locale_1.t('Recommended Searches')}</SecondaryMenuHeader>
      {/* Could only happen on self-hosted */}
      {globalSearches.length === 0 ? (<EmptyItem>{locale_1.t('No recommended searches yet.')}</EmptyItem>) : (globalSearches.map(function (search, index) { return (<SavedSearchMenuItem key={search.id} search={search} isLast={index === globalSearches.length - 1} {...props}/>); }))}
    </react_1.Fragment>);
}
exports.default = SavedSearchMenu;
var SearchTitle = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  ", "\n"], ["\n  color: ", ";\n  ", "\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default);
var SearchQueryContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, overflowEllipsis_1.default);
var SearchQuery = styled_1.default('code')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  padding: 0;\n  background: inherit;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  padding: 0;\n  background: inherit;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; });
var SearchSort = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  &:before {\n    font-size: ", ";\n    color: ", ";\n    content: ' \u2022 ';\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n  &:before {\n    font-size: ", ";\n    color: ", ";\n    content: ' \\u2022 ';\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.textColor; });
var TooltipSearchQuery = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.text.familyMono; });
var DeleteButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, space_1.default(1), function (p) { return p.theme.blue300; });
var MenuHeader = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  color: ", ";\n  background: ", ";\n  line-height: 0.75;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n"], ["\n  align-items: center;\n  color: ", ";\n  background: ", ";\n  line-height: 0.75;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.backgroundSecondary; }, space_1.default(1.5), space_1.default(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var SecondaryMenuHeader = styled_1.default(MenuHeader)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  border-radius: 0;\n"], ["\n  border-top: 1px solid ", ";\n  border-radius: 0;\n"])), function (p) { return p.theme.innerBorder; });
var StyledMenuItem = styled_1.default(menuItem_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  border-bottom: ", ";\n  font-size: ", ";\n\n  & > span {\n    padding: ", " ", ";\n  }\n\n  ", "\n"], ["\n  border-bottom: ", ";\n  font-size: ", ";\n\n  & > span {\n    padding: ", " ", ";\n  }\n\n  ", "\n"])), function (p) { return (!p.isLast ? "1px solid " + p.theme.innerBorder : null); }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(2), function (p) {
    return p.isActive &&
        "\n  " + SearchTitle + ", " + SearchQuery + ", " + SearchSort + " {\n    color: " + p.theme.white + ";\n  }\n  " + SearchSort + ":before {\n    color: " + p.theme.white + ";\n  }\n  &:hover {\n    " + SearchTitle + ", " + SearchQuery + ", " + SearchSort + " {\n      color: " + p.theme.black + ";\n    }\n    " + SearchSort + ":before {\n      color: " + p.theme.black + ";\n    }\n  }\n  ";
});
var MenuItemLink = styled_1.default('a')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: block;\n  flex-grow: 1;\n  /* Nav tabs style override */\n  border: 0;\n\n  ", "\n"], ["\n  display: block;\n  flex-grow: 1;\n  /* Nav tabs style override */\n  border: 0;\n\n  ", "\n"])), overflowEllipsis_1.default);
var EmptyItem = styled_1.default('li')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  color: ", ";\n"], ["\n  padding: ", " ", ";\n  color: ", ";\n"])), space_1.default(1), space_1.default(1.5), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=savedSearchMenu.jsx.map