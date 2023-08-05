Object.defineProperty(exports, "__esModule", { value: true });
exports.ActionButton = exports.makeSearchBuilderAction = exports.makeSaveSearchAction = exports.makePinSearchAction = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var savedSearches_1 = require("app/actionCreators/savedSearches");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var analytics_1 = require("app/utils/analytics");
var createSavedSearchModal_1 = tslib_1.__importDefault(require("app/views/issueList/createSavedSearchModal"));
var utils_1 = require("./utils");
/**
 * The Pin Search action toggles the current as a pinned search
 */
function makePinSearchAction(_a) {
    var _this = this;
    var pinnedSearch = _a.pinnedSearch, sort = _a.sort;
    var PinSearchAction = function (_a) {
        var menuItemVariant = _a.menuItemVariant, savedSearchType = _a.savedSearchType, organization = _a.organization, api = _a.api, query = _a.query, location = _a.location;
        var onTogglePinnedSearch = function (evt) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, _cursor, _page, currentQuery, resp;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        evt.preventDefault();
                        evt.stopPropagation();
                        if (savedSearchType === undefined) {
                            return [2 /*return*/];
                        }
                        _a = location.query, _cursor = _a.cursor, _page = _a.page, currentQuery = tslib_1.__rest(_a, ["cursor", "page"]);
                        analytics_1.trackAnalyticsEvent({
                            eventKey: 'search.pin',
                            eventName: 'Search: Pin',
                            organization_id: organization.id,
                            action: !!pinnedSearch ? 'unpin' : 'pin',
                            search_type: savedSearchType === types_1.SavedSearchType.ISSUE ? 'issues' : 'events',
                            query: (_b = pinnedSearch === null || pinnedSearch === void 0 ? void 0 : pinnedSearch.query) !== null && _b !== void 0 ? _b : query,
                        });
                        if (!!pinnedSearch) {
                            savedSearches_1.unpinSearch(api, organization.slug, savedSearchType, pinnedSearch).then(function () {
                                react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, location), { pathname: "/organizations/" + organization.slug + "/issues/", query: tslib_1.__assign(tslib_1.__assign({}, currentQuery), { query: pinnedSearch.query, sort: pinnedSearch.sort }) }));
                            });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, savedSearches_1.pinSearch(api, organization.slug, savedSearchType, utils_1.removeSpace(query), sort)];
                    case 1:
                        resp = _c.sent();
                        if (!resp || !resp.id) {
                            return [2 /*return*/];
                        }
                        react_router_1.browserHistory.push(tslib_1.__assign(tslib_1.__assign({}, location), { pathname: "/organizations/" + organization.slug + "/issues/searches/" + resp.id + "/", query: currentQuery }));
                        return [2 /*return*/];
                }
            });
        }); };
        var pinTooltip = !!pinnedSearch ? locale_1.t('Unpin this search') : locale_1.t('Pin this search');
        return menuItemVariant ? (<menuItem_1.default withBorder data-test-id="pin-icon" icon={<icons_1.IconPin isSolid={!!pinnedSearch} size="xs"/>} onClick={onTogglePinnedSearch}>
        {!!pinnedSearch ? locale_1.t('Unpin Search') : locale_1.t('Pin Search')}
      </menuItem_1.default>) : (<exports.ActionButton title={pinTooltip} disabled={!query} aria-label={pinTooltip} onClick={onTogglePinnedSearch} isActive={!!pinnedSearch} data-test-id="pin-icon" icon={<icons_1.IconPin isSolid={!!pinnedSearch} size="xs"/>}/>);
    };
    return { key: 'pinSearch', Action: react_router_1.withRouter(PinSearchAction) };
}
exports.makePinSearchAction = makePinSearchAction;
/**
 * The Save Search action triggers the create saved search modal from the
 * current query.
 */
function makeSaveSearchAction(_a) {
    var sort = _a.sort;
    var SavedSearchAction = function (_a) {
        var menuItemVariant = _a.menuItemVariant, query = _a.query, organization = _a.organization;
        var onClick = function () {
            return modal_1.openModal(function (deps) { return (<createSavedSearchModal_1.default {...deps} {...{ organization: organization, query: query, sort: sort }}/>); });
        };
        return (<access_1.default organization={organization} access={['org:write']}>
        {menuItemVariant ? (<menuItem_1.default withBorder icon={<icons_1.IconAdd size="xs"/>} onClick={onClick}>
            {locale_1.t('Create Saved Search')}
          </menuItem_1.default>) : (<exports.ActionButton onClick={onClick} data-test-id="save-current-search" icon={<icons_1.IconAdd size="xs"/>} title={locale_1.t('Add to organization saved searches')} aria-label={locale_1.t('Add to organization saved searches')}/>)}
      </access_1.default>);
    };
    return { key: 'saveSearch', Action: SavedSearchAction };
}
exports.makeSaveSearchAction = makeSaveSearchAction;
/**
 * The Search Builder action toggles the Issue Stream search builder
 */
function makeSearchBuilderAction(_a) {
    var onSidebarToggle = _a.onSidebarToggle;
    var SearchBuilderAction = function (_a) {
        var menuItemVariant = _a.menuItemVariant;
        return menuItemVariant ? (<menuItem_1.default withBorder icon={<icons_1.IconSliders size="xs"/>} onClick={onSidebarToggle}>
        {locale_1.t('Toggle sidebar')}
      </menuItem_1.default>) : (<exports.ActionButton title={locale_1.t('Toggle search builder')} tooltipProps={{ containerDisplayMode: 'inline-flex' }} aria-label={locale_1.t('Toggle search builder')} onClick={onSidebarToggle} icon={<icons_1.IconSliders size="xs"/>}/>);
    };
    return { key: 'searchBuilder', Action: SearchBuilderAction };
}
exports.makeSearchBuilderAction = makeSearchBuilderAction;
exports.ActionButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  width: 18px;\n\n  &,\n  &:hover,\n  &:focus {\n    background: transparent;\n  }\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  width: 18px;\n\n  &,\n  &:hover,\n  &:focus {\n    background: transparent;\n  }\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return (p.isActive ? p.theme.blue300 : p.theme.gray300); }, function (p) { return p.theme.gray400; });
exports.ActionButton.defaultProps = {
    type: 'button',
    borderless: true,
    size: 'zero',
};
var templateObject_1;
//# sourceMappingURL=actions.jsx.map