Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var panels_1 = require("app/components/panels");
var removeAtArrayIndex_1 = require("app/utils/removeAtArrayIndex");
var replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var actionsPanel_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/triggers/actionsPanel"));
var form_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/triggers/form"));
/**
 * A list of forms to add, edit, and delete triggers.
 */
var Triggers = /** @class */ (function (_super) {
    tslib_1.__extends(Triggers, _super);
    function Triggers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteTrigger = function (index) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var updatedTriggers = removeAtArrayIndex_1.removeAtArrayIndex(triggers, index);
            onChange(updatedTriggers);
        };
        _this.handleChangeTrigger = function (triggerIndex, trigger, changeObj) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var updatedTriggers = replaceAtArrayIndex_1.replaceAtArrayIndex(triggers, triggerIndex, trigger);
            onChange(updatedTriggers, triggerIndex, changeObj);
        };
        _this.handleAddAction = function (triggerIndex, action) {
            var _a = _this.props, onChange = _a.onChange, triggers = _a.triggers;
            var trigger = triggers[triggerIndex];
            var actions = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(trigger.actions)), [action]);
            var updatedTriggers = replaceAtArrayIndex_1.replaceAtArrayIndex(triggers, triggerIndex, tslib_1.__assign(tslib_1.__assign({}, trigger), { actions: actions }));
            onChange(updatedTriggers, triggerIndex, { actions: actions });
        };
        _this.handleChangeActions = function (triggerIndex, triggers, actions) {
            var onChange = _this.props.onChange;
            var trigger = triggers[triggerIndex];
            var updatedTriggers = replaceAtArrayIndex_1.replaceAtArrayIndex(triggers, triggerIndex, tslib_1.__assign(tslib_1.__assign({}, trigger), { actions: actions }));
            onChange(updatedTriggers, triggerIndex, { actions: actions });
        };
        return _this;
    }
    Triggers.prototype.render = function () {
        var _a = this.props, availableActions = _a.availableActions, currentProject = _a.currentProject, errors = _a.errors, organization = _a.organization, projects = _a.projects, triggers = _a.triggers, disabled = _a.disabled, aggregate = _a.aggregate, thresholdType = _a.thresholdType, resolveThreshold = _a.resolveThreshold, onThresholdTypeChange = _a.onThresholdTypeChange, onResolveThresholdChange = _a.onResolveThresholdChange;
        // Note we only support 2 triggers max
        return (<react_1.Fragment>
        <panels_1.Panel>
          <panels_1.PanelBody>
            <form_1.default disabled={disabled} errors={errors} organization={organization} projects={projects} triggers={triggers} aggregate={aggregate} resolveThreshold={resolveThreshold} thresholdType={thresholdType} onChange={this.handleChangeTrigger} onThresholdTypeChange={onThresholdTypeChange} onResolveThresholdChange={onResolveThresholdChange}/>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <actionsPanel_1.default disabled={disabled} loading={availableActions === null} error={false} availableActions={availableActions} currentProject={currentProject} organization={organization} projects={projects} triggers={triggers} onChange={this.handleChangeActions} onAdd={this.handleAddAction}/>
      </react_1.Fragment>);
    };
    return Triggers;
}(react_1.Component));
exports.default = withProjects_1.default(Triggers);
//# sourceMappingURL=index.jsx.map