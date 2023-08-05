Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var groupingActions_1 = tslib_1.__importDefault(require("app/actions/groupingActions"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var eventOrGroupHeader_1 = tslib_1.__importDefault(require("app/components/eventOrGroupHeader"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var groupingStore_1 = tslib_1.__importDefault(require("app/stores/groupingStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var MergedItem = /** @class */ (function (_super) {
    tslib_1.__extends(MergedItem, _super);
    function MergedItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: false,
            checked: false,
            busy: false,
        };
        _this.listener = groupingStore_1.default.listen(function (data) { return _this.onGroupChange(data); }, undefined);
        _this.onGroupChange = function (_a) {
            var unmergeState = _a.unmergeState;
            if (!unmergeState) {
                return;
            }
            var fingerprint = _this.props.fingerprint;
            var stateForId = unmergeState.has(fingerprint.id)
                ? unmergeState.get(fingerprint.id)
                : undefined;
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
        _this.handleToggleEvents = function () {
            var fingerprint = _this.props.fingerprint;
            groupingActions_1.default.toggleCollapseFingerprint(fingerprint.id);
        };
        _this.handleToggle = function () {
            var fingerprint = _this.props.fingerprint;
            var latestEvent = fingerprint.latestEvent;
            if (_this.state.busy) {
                return;
            }
            // clicking anywhere in the row will toggle the checkbox
            groupingActions_1.default.toggleUnmerge([fingerprint.id, latestEvent.id]);
        };
        return _this;
    }
    // Disable default behavior of toggling checkbox
    MergedItem.prototype.handleLabelClick = function (event) {
        event.preventDefault();
    };
    MergedItem.prototype.handleCheckClick = function () {
        // noop because of react warning about being a controlled input without `onChange`
        // we handle change via row click
    };
    MergedItem.prototype.renderFingerprint = function (id, label) {
        if (!label) {
            return id;
        }
        return (<tooltip_1.default title={id}>
        <code>{label}</code>
      </tooltip_1.default>);
    };
    MergedItem.prototype.render = function () {
        var _a = this.props, fingerprint = _a.fingerprint, organization = _a.organization;
        var latestEvent = fingerprint.latestEvent, id = fingerprint.id, label = fingerprint.label;
        var _b = this.state, collapsed = _b.collapsed, busy = _b.busy, checked = _b.checked;
        var checkboxDisabled = busy;
        // `latestEvent` can be null if last event w/ fingerprint is not within retention period
        return (<MergedGroup busy={busy}>
        <Controls expanded={!collapsed}>
          <ActionWrapper onClick={this.handleToggle}>
            <checkbox_1.default id={id} value={id} checked={checked} disabled={checkboxDisabled} onChange={this.handleCheckClick}/>

            <FingerprintLabel onClick={this.handleLabelClick} htmlFor={id}>
              {this.renderFingerprint(id, label)}
            </FingerprintLabel>
          </ActionWrapper>

          <div>
            <Collapse onClick={this.handleToggleEvents}>
              <icons_1.IconChevron direction={collapsed ? 'down' : 'up'} size="xs"/>
            </Collapse>
          </div>
        </Controls>

        {!collapsed && (<MergedEventList className="event-list">
            {latestEvent && (<EventDetails className="event-details">
                <eventOrGroupHeader_1.default data={latestEvent} organization={organization} hideIcons hideLevel/>
              </EventDetails>)}
          </MergedEventList>)}
      </MergedGroup>);
    };
    return MergedItem;
}(React.Component));
var MergedGroup = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return p.busy && 'opacity: 0.2'; });
var ActionWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n\n  /* Can't use styled components for this because of broad selector */\n  input[type='checkbox'] {\n    margin: 0;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n\n  /* Can't use styled components for this because of broad selector */\n  input[type='checkbox'] {\n    margin: 0;\n  }\n"])), space_1.default(1));
var Controls = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  border-top: 1px solid ", ";\n  background-color: ", ";\n  padding: ", " ", ";\n  ", ";\n\n  ", " {\n    &:first-child & {\n      border-top: none;\n    }\n    &:last-child & {\n      border-top: none;\n      border-bottom: 1px solid ", ";\n    }\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  border-top: 1px solid ", ";\n  background-color: ", ";\n  padding: ", " ", ";\n  ", ";\n\n  ", " {\n    &:first-child & {\n      border-top: none;\n    }\n    &:last-child & {\n      border-top: none;\n      border-bottom: 1px solid ", ";\n    }\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.gray100; }, space_1.default(0.5), space_1.default(1), function (p) { return p.expanded && "border-bottom: 1px solid " + p.theme.innerBorder; }, MergedGroup, function (p) { return p.theme.innerBorder; });
var FingerprintLabel = styled_1.default('label')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n\n  ", " & {\n    font-weight: 400;\n    margin: 0;\n  }\n"], ["\n  font-family: ", ";\n\n  " /* sc-selector */, " & {\n    font-weight: 400;\n    margin: 0;\n  }\n"])), function (p) { return p.theme.text.familyMono; }, /* sc-selector */ Controls);
var Collapse = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n"], ["\n  cursor: pointer;\n"])));
var MergedEventList = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  border: none;\n"], ["\n  overflow: hidden;\n  border: none;\n"])));
var EventDetails = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n\n  .event-list & {\n    padding: ", ";\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n\n  .event-list & {\n    padding: ", ";\n  }\n"])), space_1.default(1));
exports.default = MergedItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=mergedItem.jsx.map