Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var groupingStore_1 = tslib_1.__importDefault(require("app/stores/groupingStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var MergedToolbar = /** @class */ (function (_super) {
    tslib_1.__extends(MergedToolbar, _super);
    function MergedToolbar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.listener = groupingStore_1.default.listen(function (data) { return _this.onGroupChange(data); }, undefined);
        _this.onGroupChange = function (updateObj) {
            var allowedKeys = [
                'unmergeLastCollapsed',
                'unmergeDisabled',
                'unmergeList',
                'enableFingerprintCompare',
            ];
            _this.setState(pick_1.default(updateObj, allowedKeys));
        };
        _this.handleShowDiff = function (event) {
            var _a = _this.props, groupId = _a.groupId, project = _a.project, orgId = _a.orgId;
            var unmergeList = _this.state.unmergeList;
            var entries = unmergeList.entries();
            // `unmergeList` should only have 2 items in map
            if (unmergeList.size !== 2) {
                return;
            }
            // only need eventId, not fingerprint
            var _b = tslib_1.__read(Array.from(entries).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), eventId = _b[1];
                return eventId;
            }), 2), baseEventId = _b[0], targetEventId = _b[1];
            modal_1.openDiffModal({
                targetIssueId: groupId,
                project: project,
                baseIssueId: groupId,
                orgId: orgId,
                baseEventId: baseEventId,
                targetEventId: targetEventId,
            });
            event.stopPropagation();
        };
        return _this;
    }
    MergedToolbar.prototype.getInitialState = function () {
        var unmergeList = groupingStore_1.default.unmergeList, unmergeLastCollapsed = groupingStore_1.default.unmergeLastCollapsed, unmergeDisabled = groupingStore_1.default.unmergeDisabled, enableFingerprintCompare = groupingStore_1.default.enableFingerprintCompare;
        return {
            enableFingerprintCompare: enableFingerprintCompare,
            unmergeList: unmergeList,
            unmergeLastCollapsed: unmergeLastCollapsed,
            unmergeDisabled: unmergeDisabled,
        };
    };
    MergedToolbar.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.listener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    MergedToolbar.prototype.render = function () {
        var _a = this.props, onUnmerge = _a.onUnmerge, onToggleCollapse = _a.onToggleCollapse;
        var _b = this.state, unmergeList = _b.unmergeList, unmergeLastCollapsed = _b.unmergeLastCollapsed, unmergeDisabled = _b.unmergeDisabled, enableFingerprintCompare = _b.enableFingerprintCompare;
        var unmergeCount = (unmergeList && unmergeList.size) || 0;
        return (<panels_1.PanelHeader hasButtons>
        <div>
          <confirm_1.default disabled={unmergeDisabled} onConfirm={onUnmerge} message={locale_1.t('These events will be unmerged and grouped into a new issue. Are you sure you want to unmerge these events?')}>
            <button_1.default size="small" title={locale_1.tct('Unmerging [unmergeCount] events', { unmergeCount: unmergeCount })}>
              {locale_1.t('Unmerge')} ({unmergeCount || 0})
            </button_1.default>
          </confirm_1.default>

          <CompareButton size="small" disabled={!enableFingerprintCompare} onClick={this.handleShowDiff}>
            {locale_1.t('Compare')}
          </CompareButton>
        </div>
        <button_1.default size="small" onClick={onToggleCollapse}>
          {unmergeLastCollapsed ? locale_1.t('Expand All') : locale_1.t('Collapse All')}
        </button_1.default>
      </panels_1.PanelHeader>);
    };
    return MergedToolbar;
}(React.Component));
exports.default = MergedToolbar;
var CompareButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=mergedToolbar.jsx.map