Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var selectMembers_1 = tslib_1.__importDefault(require("app/components/selectMembers"));
var types_1 = require("app/views/alerts/incidentRules/types");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var getPlaceholderForType = function (type) {
    switch (type) {
        case types_1.ActionType.SLACK:
            return '@username or #channel';
        case types_1.ActionType.MSTEAMS:
            // no prefixes for msteams
            return 'username or channel';
        case types_1.ActionType.PAGERDUTY:
            return 'service';
        default:
            throw Error('Not implemented');
    }
};
function ActionTargetSelector(props) {
    var action = props.action, availableAction = props.availableAction, disabled = props.disabled, loading = props.loading, onChange = props.onChange, organization = props.organization, project = props.project;
    var handleChangeTargetIdentifier = function (value) {
        onChange(value.value);
    };
    var handleChangeSpecificTargetIdentifier = function (e) {
        onChange(e.target.value);
    };
    switch (action.targetType) {
        case types_1.TargetType.TEAM:
        case types_1.TargetType.USER:
            var isTeam = action.targetType === types_1.TargetType.TEAM;
            return (<selectMembers_1.default disabled={disabled} key={isTeam ? 'team' : 'member'} showTeam={isTeam} project={project} organization={organization} value={action.targetIdentifier} onChange={handleChangeTargetIdentifier}/>);
        case types_1.TargetType.SPECIFIC:
            return (availableAction === null || availableAction === void 0 ? void 0 : availableAction.options) ? (<selectControl_1.default isDisabled={disabled || loading} value={action.targetIdentifier} options={availableAction.options} onChange={handleChangeTargetIdentifier}/>) : (<input_1.default type="text" autoComplete="off" disabled={disabled} key={action.type} value={action.targetIdentifier || ''} onChange={handleChangeSpecificTargetIdentifier} placeholder={getPlaceholderForType(action.type)}/>);
        default:
            return null;
    }
}
exports.default = ActionTargetSelector;
//# sourceMappingURL=actionTargetSelector.jsx.map