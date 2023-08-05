Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("../utils");
var statusTooltip_1 = tslib_1.__importDefault(require("./status/statusTooltip"));
var actions_1 = tslib_1.__importDefault(require("./actions"));
var information_1 = tslib_1.__importDefault(require("./information"));
function Candidate(_a) {
    var candidate = _a.candidate, builtinSymbolSources = _a.builtinSymbolSources, organization = _a.organization, projectId = _a.projectId, baseUrl = _a.baseUrl, haveCandidatesAtLeastOneAction = _a.haveCandidatesAtLeastOneAction, hasReprocessWarning = _a.hasReprocessWarning, onDelete = _a.onDelete, eventDateReceived = _a.eventDateReceived;
    var source = candidate.source;
    var isInternalSource = source === utils_1.INTERNAL_SOURCE;
    return (<react_1.Fragment>
      <Column>
        <statusTooltip_1.default candidate={candidate} hasReprocessWarning={hasReprocessWarning}/>
      </Column>

      <InformationColumn>
        <information_1.default candidate={candidate} builtinSymbolSources={builtinSymbolSources} isInternalSource={isInternalSource} eventDateReceived={eventDateReceived} hasReprocessWarning={hasReprocessWarning}/>
      </InformationColumn>

      {haveCandidatesAtLeastOneAction && (<ActionsColumn>
          <actions_1.default onDelete={onDelete} baseUrl={baseUrl} projectId={projectId} organization={organization} candidate={candidate} isInternalSource={isInternalSource}/>
        </ActionsColumn>)}
    </react_1.Fragment>);
}
exports.default = Candidate;
var Column = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var InformationColumn = styled_1.default(Column)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-direction: column;\n  align-items: flex-start;\n"], ["\n  flex-direction: column;\n  align-items: flex-start;\n"])));
var ActionsColumn = styled_1.default(Column)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map