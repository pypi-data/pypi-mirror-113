Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var modal_1 = require("app/actionCreators/modal");
var groupingActions_1 = tslib_1.__importDefault(require("app/actions/groupingActions"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var eventOrGroupExtraDetails_1 = tslib_1.__importDefault(require("app/components/eventOrGroupExtraDetails"));
var eventOrGroupHeader_1 = tslib_1.__importDefault(require("app/components/eventOrGroupHeader"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var panels_1 = require("app/components/panels");
var scoreBar_1 = tslib_1.__importDefault(require("app/components/scoreBar"));
var similarScoreCard_1 = tslib_1.__importDefault(require("app/components/similarScoreCard"));
var locale_1 = require("app/locale");
var groupingStore_1 = tslib_1.__importDefault(require("app/stores/groupingStore"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var initialState = { visible: true, checked: false, busy: false };
var Item = /** @class */ (function (_super) {
    tslib_1.__extends(Item, _super);
    function Item() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.listener = groupingStore_1.default.listen(function (data) { return _this.onGroupChange(data); }, undefined);
        _this.handleToggle = function () {
            var issue = _this.props.issue;
            // clicking anywhere in the row will toggle the checkbox
            if (!_this.state.busy) {
                groupingActions_1.default.toggleMerge(issue.id);
            }
        };
        _this.handleShowDiff = function (event) {
            var _a = _this.props, orgId = _a.orgId, baseIssueId = _a.groupId, issue = _a.issue, project = _a.project;
            var targetIssueId = issue.id;
            modal_1.openDiffModal({ baseIssueId: baseIssueId, targetIssueId: targetIssueId, project: project, orgId: orgId });
            event.stopPropagation();
        };
        _this.handleCheckClick = function () {
            // noop to appease React warnings
            // This is controlled via row click instead of only Checkbox
        };
        _this.onGroupChange = function (_a) {
            var mergeState = _a.mergeState;
            if (!mergeState) {
                return;
            }
            var issue = _this.props.issue;
            var stateForId = mergeState.has(issue.id) && mergeState.get(issue.id);
            if (!stateForId) {
                return;
            }
            Object.keys(stateForId).forEach(function (key) {
                if (stateForId[key] === _this.state[key]) {
                    return;
                }
                _this.setState(function (prevState) {
                    var _a;
                    return (tslib_1.__assign(tslib_1.__assign({}, prevState), (_a = {}, _a[key] = stateForId[key], _a)));
                });
            });
        };
        return _this;
    }
    Item.prototype.componentWillUnmount = function () {
        callIfFunction_1.callIfFunction(this.listener);
    };
    Item.prototype.render = function () {
        var _a = this.props, aggregate = _a.aggregate, scoresByInterface = _a.scoresByInterface, issue = _a.issue, v2 = _a.v2;
        var _b = this.state, visible = _b.visible, busy = _b.busy;
        var similarInterfaces = v2 ? ['similarity'] : ['exception', 'message'];
        if (!visible) {
            return null;
        }
        var cx = classnames_1.default('group', {
            isResolved: issue.status === 'resolved',
            busy: busy,
        });
        return (<StyledPanelItem data-test-id="similar-item-row" className={cx} onClick={this.handleToggle}>
        <Details>
          <checkbox_1.default id={issue.id} value={issue.id} checked={this.state.checked} onChange={this.handleCheckClick}/>
          <EventDetails>
            <eventOrGroupHeader_1.default data={issue} includeLink size="normal"/>
            <eventOrGroupExtraDetails_1.default data={tslib_1.__assign(tslib_1.__assign({}, issue), { lastSeen: '' })} showAssignee/>
          </EventDetails>

          <Diff>
            <button_1.default onClick={this.handleShowDiff} size="small">
              {locale_1.t('Diff')}
            </button_1.default>
          </Diff>
        </Details>

        <Columns>
          <StyledCount value={issue.count}/>

          {similarInterfaces.map(function (interfaceName) {
                var avgScore = aggregate === null || aggregate === void 0 ? void 0 : aggregate[interfaceName];
                var scoreList = (scoresByInterface === null || scoresByInterface === void 0 ? void 0 : scoresByInterface[interfaceName]) || [];
                // Check for valid number (and not NaN)
                var scoreValue = typeof avgScore === 'number' && !Number.isNaN(avgScore) ? avgScore : 0;
                return (<Column key={interfaceName}>
                <hovercard_1.default body={scoreList.length && <similarScoreCard_1.default scoreList={scoreList}/>}>
                  <scoreBar_1.default vertical score={Math.round(scoreValue * 5)}/>
                </hovercard_1.default>
              </Column>);
            })}
        </Columns>
      </StyledPanelItem>);
    };
    return Item;
}(React.Component));
var Details = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n\n  display: grid;\n  gap: ", ";\n  grid-template-columns: max-content auto max-content;\n  margin-left: ", ";\n\n  input[type='checkbox'] {\n    margin: 0;\n  }\n"], ["\n  ", ";\n\n  display: grid;\n  gap: ", ";\n  grid-template-columns: max-content auto max-content;\n  margin-left: ", ";\n\n  input[type='checkbox'] {\n    margin: 0;\n  }\n"])), overflowEllipsis_1.default, space_1.default(1), space_1.default(2));
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " 0;\n"], ["\n  padding: ", " 0;\n"])), space_1.default(1));
var Columns = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"])));
var columnStyle = react_1.css(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"], ["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"])), space_1.default(0.5));
var Column = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), columnStyle);
var StyledCount = styled_1.default(count_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), columnStyle);
var Diff = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"])), space_1.default(0.25));
var EventDetails = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  ", ";\n"], ["\n  flex: 1;\n  ", ";\n"])), overflowEllipsis_1.default);
exports.default = Item;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=item.jsx.map