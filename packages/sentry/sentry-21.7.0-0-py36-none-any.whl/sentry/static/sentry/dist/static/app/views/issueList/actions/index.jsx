Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListActions = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var uniq_1 = tslib_1.__importDefault(require("lodash/uniq"));
var group_1 = require("app/actionCreators/group");
var indicator_1 = require("app/actionCreators/indicator");
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var selectedGroupStore_1 = tslib_1.__importDefault(require("app/stores/selectedGroupStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var actionSet_1 = tslib_1.__importDefault(require("./actionSet"));
var headers_1 = tslib_1.__importDefault(require("./headers"));
var utils_1 = require("./utils");
var IssueListActions = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListActions, _super);
    function IssueListActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            anySelected: false,
            multiSelected: false,
            pageSelected: false,
            allInQuerySelected: false,
            selectedIds: new Set(),
        };
        _this.listener = selectedGroupStore_1.default.listen(function () { return _this.handleSelectedGroupChange(); }, undefined);
        _this.handleSelectStatsPeriod = function (period) {
            return _this.props.onSelectStatsPeriod(period);
        };
        _this.handleApplyToAll = function () {
            _this.setState({ allInQuerySelected: true });
        };
        _this.handleUpdate = function (data) {
            var _a = _this.props, selection = _a.selection, api = _a.api, organization = _a.organization, query = _a.query, onMarkReviewed = _a.onMarkReviewed;
            var orgId = organization.slug;
            _this.actionSelectedGroups(function (itemIds) {
                indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
                if ((data === null || data === void 0 ? void 0 : data.inbox) === false) {
                    onMarkReviewed === null || onMarkReviewed === void 0 ? void 0 : onMarkReviewed(itemIds !== null && itemIds !== void 0 ? itemIds : []);
                }
                // If `itemIds` is undefined then it means we expect to bulk update all items
                // that match the query.
                //
                // We need to always respect the projects selected in the global selection header:
                // * users with no global views requires a project to be specified
                // * users with global views need to be explicit about what projects the query will run against
                var projectConstraints = { project: selection.projects };
                group_1.bulkUpdate(api, tslib_1.__assign(tslib_1.__assign({ orgId: orgId, itemIds: itemIds, data: data, query: query, environment: selection.environments }, projectConstraints), selection.datetime), {
                    complete: function () {
                        indicator_1.clearIndicators();
                    },
                });
            });
        };
        _this.handleDelete = function () {
            var _a = _this.props, selection = _a.selection, api = _a.api, organization = _a.organization, query = _a.query, onDelete = _a.onDelete;
            var orgId = organization.slug;
            indicator_1.addLoadingMessage(locale_1.t('Removing events\u2026'));
            _this.actionSelectedGroups(function (itemIds) {
                group_1.bulkDelete(api, tslib_1.__assign({ orgId: orgId, itemIds: itemIds, query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: function () {
                        indicator_1.clearIndicators();
                        onDelete();
                    },
                });
            });
        };
        _this.handleMerge = function () {
            var _a = _this.props, selection = _a.selection, api = _a.api, organization = _a.organization, query = _a.query;
            var orgId = organization.slug;
            indicator_1.addLoadingMessage(locale_1.t('Merging events\u2026'));
            _this.actionSelectedGroups(function (itemIds) {
                group_1.mergeGroups(api, tslib_1.__assign({ orgId: orgId, itemIds: itemIds, query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: function () {
                        indicator_1.clearIndicators();
                    },
                });
            });
        };
        _this.shouldConfirm = function (action) {
            var selectedItems = selectedGroupStore_1.default.getSelectedIds();
            switch (action) {
                case utils_1.ConfirmAction.RESOLVE:
                case utils_1.ConfirmAction.UNRESOLVE:
                case utils_1.ConfirmAction.IGNORE:
                case utils_1.ConfirmAction.UNBOOKMARK: {
                    var pageSelected = _this.state.pageSelected;
                    return pageSelected && selectedItems.size > 1;
                }
                case utils_1.ConfirmAction.BOOKMARK:
                    return selectedItems.size > 1;
                case utils_1.ConfirmAction.MERGE:
                case utils_1.ConfirmAction.DELETE:
                default:
                    return true; // By default, should confirm ...
            }
        };
        return _this;
    }
    IssueListActions.prototype.componentDidMount = function () {
        this.handleSelectedGroupChange();
    };
    IssueListActions.prototype.componentWillUnmount = function () {
        callIfFunction_1.callIfFunction(this.listener);
    };
    IssueListActions.prototype.actionSelectedGroups = function (callback) {
        var selectedIds;
        if (this.state.allInQuerySelected) {
            selectedIds = undefined; // undefined means "all"
        }
        else {
            var itemIdSet_1 = selectedGroupStore_1.default.getSelectedIds();
            selectedIds = this.props.groupIds.filter(function (itemId) { return itemIdSet_1.has(itemId); });
        }
        callback(selectedIds);
        this.deselectAll();
    };
    IssueListActions.prototype.deselectAll = function () {
        selectedGroupStore_1.default.deselectAll();
        this.setState({ allInQuerySelected: false });
    };
    // Handler for when `SelectedGroupStore` changes
    IssueListActions.prototype.handleSelectedGroupChange = function () {
        var selected = selectedGroupStore_1.default.getSelectedIds();
        var projects = tslib_1.__spreadArray([], tslib_1.__read(selected)).map(function (id) { return groupStore_1.default.get(id); })
            .filter(function (group) { return !!(group && group.project); })
            .map(function (group) { return group.project.slug; });
        var uniqProjects = uniq_1.default(projects);
        // we only want selectedProjectSlug set if there is 1 project
        // more or fewer should result in a null so that the action toolbar
        // can behave correctly.
        var selectedProjectSlug = uniqProjects.length === 1 ? uniqProjects[0] : undefined;
        this.setState({
            pageSelected: selectedGroupStore_1.default.allSelected(),
            multiSelected: selectedGroupStore_1.default.multiSelected(),
            anySelected: selectedGroupStore_1.default.anySelected(),
            allInQuerySelected: false,
            selectedIds: selectedGroupStore_1.default.getSelectedIds(),
            selectedProjectSlug: selectedProjectSlug,
        });
    };
    IssueListActions.prototype.handleSelectAll = function () {
        selectedGroupStore_1.default.toggleSelectAll();
    };
    IssueListActions.prototype.render = function () {
        var _a = this.props, allResultsVisible = _a.allResultsVisible, queryCount = _a.queryCount, query = _a.query, statsPeriod = _a.statsPeriod, selection = _a.selection, organization = _a.organization, displayReprocessingActions = _a.displayReprocessingActions;
        var _b = this.state, allInQuerySelected = _b.allInQuerySelected, anySelected = _b.anySelected, pageSelected = _b.pageSelected, issues = _b.selectedIds, multiSelected = _b.multiSelected, selectedProjectSlug = _b.selectedProjectSlug;
        var numIssues = issues.size;
        return (<Sticky>
        <StyledFlex>
          <ActionsCheckbox>
            <checkbox_1.default onChange={this.handleSelectAll} checked={pageSelected} disabled={displayReprocessingActions}/>
          </ActionsCheckbox>
          {!displayReprocessingActions && (<actionSet_1.default orgSlug={organization.slug} queryCount={queryCount} query={query} issues={issues} allInQuerySelected={allInQuerySelected} anySelected={anySelected} multiSelected={multiSelected} selectedProjectSlug={selectedProjectSlug} onShouldConfirm={this.shouldConfirm} onDelete={this.handleDelete} onMerge={this.handleMerge} onUpdate={this.handleUpdate}/>)}
          <headers_1.default onSelectStatsPeriod={this.handleSelectStatsPeriod} anySelected={anySelected} selection={selection} statsPeriod={statsPeriod} isReprocessingQuery={displayReprocessingActions}/>
        </StyledFlex>
        {!allResultsVisible && pageSelected && (<SelectAllNotice>
            {allInQuerySelected ? (queryCount >= utils_1.BULK_LIMIT ? (locale_1.tct('Selected up to the first [count] issues that match this search query.', {
                    count: utils_1.BULK_LIMIT_STR,
                })) : (locale_1.tct('Selected all [count] issues that match this search query.', {
                    count: queryCount,
                }))) : (<React.Fragment>
                {locale_1.tn('%s issue on this page selected.', '%s issues on this page selected.', numIssues)}
                <SelectAllLink onClick={this.handleApplyToAll}>
                  {queryCount >= utils_1.BULK_LIMIT
                        ? locale_1.tct('Select the first [count] issues that match this search query.', {
                            count: utils_1.BULK_LIMIT_STR,
                        })
                        : locale_1.tct('Select all [count] issues that match this search query.', {
                            count: queryCount,
                        })}
                </SelectAllLink>
              </React.Fragment>)}
          </SelectAllNotice>)}
      </Sticky>);
    };
    return IssueListActions;
}(React.Component));
exports.IssueListActions = IssueListActions;
var Sticky = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: sticky;\n  z-index: ", ";\n  top: -1px;\n"], ["\n  position: sticky;\n  z-index: ", ";\n  top: -1px;\n"])), function (p) { return p.theme.zIndex.header; });
var StyledFlex = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  box-sizing: border-box;\n  min-height: 45px;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  align-items: center;\n  background: ", ";\n  border: 1px solid ", ";\n  border-top: none;\n  border-radius: ", " ", " 0 0;\n  margin: 0 -1px -1px;\n"], ["\n  display: flex;\n  box-sizing: border-box;\n  min-height: 45px;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  align-items: center;\n  background: ", ";\n  border: 1px solid ", ";\n  border-top: none;\n  border-radius: ", " ", " 0 0;\n  margin: 0 -1px -1px;\n"])), space_1.default(1), space_1.default(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var ActionsCheckbox = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding-left: ", ";\n  margin-bottom: 1px;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"], ["\n  padding-left: ", ";\n  margin-bottom: 1px;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"])), space_1.default(2));
var SelectAllNotice = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n  color: ", ";\n  font-size: ", ";\n  text-align: center;\n  padding: ", " ", ";\n"], ["\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n  color: ", ";\n  font-size: ", ";\n  text-align: center;\n  padding: ", " ", ";\n"])), function (p) { return p.theme.yellow100; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.black; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5), space_1.default(1.5));
var SelectAllLink = styled_1.default('a')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
exports.default = withApi_1.default(IssueListActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map