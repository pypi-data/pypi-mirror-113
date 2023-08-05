Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var guid_1 = require("app/utils/guid");
var removeAtArrayIndex_1 = require("app/utils/removeAtArrayIndex");
var replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var actionTargetSelector_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/triggers/actionsPanel/actionTargetSelector"));
var deleteActionButton_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/triggers/actionsPanel/deleteActionButton"));
var types_1 = require("app/views/alerts/incidentRules/types");
/**
 * When a new action is added, all of it's settings should be set to their default values.
 * @param actionConfig
 * @param dateCreated kept to maintain order of unsaved actions
 */
var getCleanAction = function (actionConfig, dateCreated) {
    return {
        unsavedId: guid_1.uniqueId(),
        unsavedDateCreated: dateCreated !== null && dateCreated !== void 0 ? dateCreated : new Date().toISOString(),
        type: actionConfig.type,
        targetType: actionConfig &&
            actionConfig.allowedTargetTypes &&
            actionConfig.allowedTargetTypes.length > 0
            ? actionConfig.allowedTargetTypes[0]
            : null,
        targetIdentifier: actionConfig.sentryAppId || '',
        integrationId: actionConfig.integrationId,
        sentryAppId: actionConfig.sentryAppId,
        options: actionConfig.options || null,
    };
};
/**
 * Actions have a type (e.g. email, slack, etc), but only some have
 * an integrationId (e.g. email is null). This helper creates a unique
 * id based on the type and integrationId so that we know what action
 * a user's saved action corresponds to.
 */
var getActionUniqueKey = function (_a) {
    var type = _a.type, integrationId = _a.integrationId, sentryAppId = _a.sentryAppId;
    if (integrationId) {
        return type + "-" + integrationId;
    }
    else if (sentryAppId) {
        return type + "-" + sentryAppId;
    }
    return type;
};
/**
 * Creates a human-friendly display name for the integration based on type and
 * server provided `integrationName`
 *
 * e.g. for slack we show that it is slack and the `integrationName` is the workspace name
 */
var getFullActionTitle = function (_a) {
    var type = _a.type, integrationName = _a.integrationName, sentryAppName = _a.sentryAppName, status = _a.status;
    if (sentryAppName) {
        if (status) {
            return sentryAppName + " (" + status + ")";
        }
        return "" + sentryAppName;
    }
    var label = types_1.ActionLabel[type];
    if (integrationName) {
        return label + " - " + integrationName;
    }
    return label;
};
/**
 * Lists saved actions as well as control to add a new action
 */
var ActionsPanel = /** @class */ (function (_super) {
    tslib_1.__extends(ActionsPanel, _super);
    function ActionsPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddAction = function () {
            var _a = _this.props, availableActions = _a.availableActions, onAdd = _a.onAdd;
            var actionConfig = availableActions === null || availableActions === void 0 ? void 0 : availableActions[0];
            if (!actionConfig) {
                indicator_1.addErrorMessage(locale_1.t('There was a problem adding an action'));
                Sentry.captureException(new Error('Unable to add an action'));
                return;
            }
            var action = getCleanAction(actionConfig);
            // Add new actions to critical by default
            var triggerIndex = 0;
            onAdd(triggerIndex, action);
        };
        _this.handleDeleteAction = function (triggerIndex, index) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var actions = triggers[triggerIndex].actions;
            onChange(triggerIndex, triggers, removeAtArrayIndex_1.removeAtArrayIndex(actions, index));
        };
        _this.handleChangeActionLevel = function (triggerIndex, index, value) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            // Convert saved action to unsaved by removing id
            var _b = triggers[triggerIndex].actions[index], _ = _b.id, action = tslib_1.__rest(_b, ["id"]);
            action.unsavedId = guid_1.uniqueId();
            triggers[value.value].actions.push(action);
            onChange(value.value, triggers, triggers[value.value].actions);
            _this.handleDeleteAction(triggerIndex, index);
        };
        _this.handleChangeActionType = function (triggerIndex, index, value) {
            var _a;
            var _b = _this.props, triggers = _b.triggers, onChange = _b.onChange, availableActions = _b.availableActions;
            var actions = triggers[triggerIndex].actions;
            var actionConfig = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(function (availableAction) { return getActionUniqueKey(availableAction) === value.value; });
            if (!actionConfig) {
                indicator_1.addErrorMessage(locale_1.t('There was a problem changing an action'));
                Sentry.captureException(new Error('Unable to change an action type'));
                return;
            }
            var existingDateCreated = (_a = actions[index].dateCreated) !== null && _a !== void 0 ? _a : actions[index].unsavedDateCreated;
            var newAction = getCleanAction(actionConfig, existingDateCreated);
            onChange(triggerIndex, triggers, replaceAtArrayIndex_1.replaceAtArrayIndex(actions, index, newAction));
        };
        _this.handleChangeTarget = function (triggerIndex, index, value) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var actions = triggers[triggerIndex].actions;
            var newAction = tslib_1.__assign(tslib_1.__assign({}, actions[index]), { targetType: value.value, targetIdentifier: '' });
            onChange(triggerIndex, triggers, replaceAtArrayIndex_1.replaceAtArrayIndex(actions, index, newAction));
        };
        return _this;
    }
    ActionsPanel.prototype.handleChangeTargetIdentifier = function (triggerIndex, index, value) {
        var _a = this.props, triggers = _a.triggers, onChange = _a.onChange;
        var actions = triggers[triggerIndex].actions;
        var newAction = tslib_1.__assign(tslib_1.__assign({}, actions[index]), { targetIdentifier: value });
        onChange(triggerIndex, triggers, replaceAtArrayIndex_1.replaceAtArrayIndex(actions, index, newAction));
    };
    ActionsPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, availableActions = _a.availableActions, currentProject = _a.currentProject, disabled = _a.disabled, loading = _a.loading, organization = _a.organization, projects = _a.projects, triggers = _a.triggers;
        var project = projects.find(function (_a) {
            var slug = _a.slug;
            return slug === currentProject;
        });
        var items = availableActions === null || availableActions === void 0 ? void 0 : availableActions.map(function (availableAction) { return ({
            value: getActionUniqueKey(availableAction),
            label: getFullActionTitle(availableAction),
        }); });
        var levels = [
            { value: 0, label: 'Critical Status' },
            { value: 1, label: 'Warning Status' },
        ];
        // Create single array of unsaved and saved trigger actions
        // Sorted by date created ascending
        var actions = triggers
            .flatMap(function (trigger, triggerIndex) {
            return trigger.actions.map(function (action, actionIdx) {
                var _a;
                var availableAction = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(function (a) { return getActionUniqueKey(a) === getActionUniqueKey(action); });
                return {
                    dateCreated: new Date((_a = action.dateCreated) !== null && _a !== void 0 ? _a : action.unsavedDateCreated).getTime(),
                    triggerIndex: triggerIndex,
                    action: action,
                    actionIdx: actionIdx,
                    availableAction: availableAction,
                };
            });
        })
            .sort(function (a, b) { return a.dateCreated - b.dateCreated; });
        return (<react_1.Fragment>
        <PerformActionsListItem>
          {locale_1.t('Perform actions')}
          <AlertParagraph>
            {locale_1.t('When any of the thresholds above are met, perform an action such as sending an email or using an integration.')}
          </AlertParagraph>
        </PerformActionsListItem>
        {loading && <loadingIndicator_1.default />}
        {actions.map(function (_a) {
                var _b, _c;
                var action = _a.action, actionIdx = _a.actionIdx, triggerIndex = _a.triggerIndex, availableAction = _a.availableAction;
                return (<div key={(_b = action.id) !== null && _b !== void 0 ? _b : action.unsavedId}>
              <RuleRowContainer>
                <PanelItemGrid>
                  <PanelItemSelects>
                    <selectControl_1.default name="select-level" aria-label={locale_1.t('Select a status level')} isDisabled={disabled || loading} placeholder={locale_1.t('Select Level')} onChange={_this.handleChangeActionLevel.bind(_this, triggerIndex, actionIdx)} value={triggerIndex} options={levels}/>
                    <selectControl_1.default name="select-action" aria-label={locale_1.t('Select an Action')} isDisabled={disabled || loading} placeholder={locale_1.t('Select Action')} onChange={_this.handleChangeActionType.bind(_this, triggerIndex, actionIdx)} value={getActionUniqueKey(action)} options={items !== null && items !== void 0 ? items : []}/>

                    {availableAction && availableAction.allowedTargetTypes.length > 1 ? (<selectControl_1.default isDisabled={disabled || loading} value={action.targetType} options={(_c = availableAction === null || availableAction === void 0 ? void 0 : availableAction.allowedTargetTypes) === null || _c === void 0 ? void 0 : _c.map(function (allowedType) { return ({
                            value: allowedType,
                            label: types_1.TargetLabel[allowedType],
                        }); })} onChange={_this.handleChangeTarget.bind(_this, triggerIndex, actionIdx)}/>) : null}
                    <actionTargetSelector_1.default action={action} availableAction={availableAction} disabled={disabled} loading={loading} onChange={_this.handleChangeTargetIdentifier.bind(_this, triggerIndex, actionIdx)} organization={organization} project={project}/>
                  </PanelItemSelects>
                  <deleteActionButton_1.default triggerIndex={triggerIndex} index={actionIdx} onClick={_this.handleDeleteAction} disabled={disabled}/>
                </PanelItemGrid>
              </RuleRowContainer>
            </div>);
            })}
        <ActionSection>
          <button_1.default type="button" disabled={disabled || loading} icon={<icons_1.IconAdd isCircled color="gray300"/>} onClick={this.handleAddAction}>
            {locale_1.t('Add Action')}
          </button_1.default>
        </ActionSection>
      </react_1.Fragment>);
    };
    return ActionsPanel;
}(react_1.PureComponent));
var ActionsPanelWithSpace = styled_1.default(ActionsPanel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(4));
var ActionSection = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(1), space_1.default(3));
var AlertParagraph = styled_1.default('p')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.subText; }, space_1.default(1), function (p) { return p.theme.fontSizeLarge; });
var PanelItemGrid = styled_1.default(panels_1.PanelItem)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  border-bottom: 0;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  border-bottom: 0;\n  padding: ", ";\n"])), space_1.default(1));
var PanelItemSelects = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-right: ", ";\n  > * {\n    flex: 0 1 200px;\n\n    &:not(:last-child) {\n      margin-right: ", ";\n    }\n  }\n"], ["\n  display: flex;\n  width: 100%;\n  margin-right: ", ";\n  > * {\n    flex: 0 1 200px;\n\n    &:not(:last-child) {\n      margin-right: ", ";\n    }\n  }\n"])), space_1.default(1), space_1.default(1));
var RuleRowContainer = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  border-radius: ", ";\n  border: 1px ", " solid;\n"], ["\n  background-color: ", ";\n  border-radius: ", ";\n  border: 1px ", " solid;\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.border; });
var StyledListItem = styled_1.default(listItem_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0 ", " 0;\n  font-size: ", ";\n"], ["\n  margin: ", " 0 ", " 0;\n  font-size: ", ";\n"])), space_1.default(2), space_1.default(3), function (p) { return p.theme.fontSizeExtraLarge; });
var PerformActionsListItem = styled_1.default(StyledListItem)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  line-height: 1.3;\n"], ["\n  margin-bottom: 0;\n  line-height: 1.3;\n"])));
exports.default = withOrganization_1.default(ActionsPanelWithSpace);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=index.jsx.map