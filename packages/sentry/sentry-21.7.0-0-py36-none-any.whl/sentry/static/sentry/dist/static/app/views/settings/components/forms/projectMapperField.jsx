Object.defineProperty(exports, "__esModule", { value: true });
exports.RenderField = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var removeAtArrayIndex_1 = require("app/utils/removeAtArrayIndex");
var fieldErrorReason_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldErrorReason"));
var controlState_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField/controlState"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
// Get the icon
var getIcon = function (iconType) {
    switch (iconType) {
        case 'vercel':
            return <icons_1.IconVercel />;
        default:
            return <icons_1.IconGeneric />;
    }
};
var RenderField = /** @class */ (function (_super) {
    tslib_1.__extends(RenderField, _super);
    function RenderField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { selectedSentryProjectId: null, selectedMappedValue: null };
        return _this;
    }
    RenderField.prototype.render = function () {
        var _this = this;
        var _a = this.props, onChange = _a.onChange, onBlur = _a.onBlur, incomingValues = _a.value, sentryProjects = _a.sentryProjects, _b = _a.mappedDropdown, mappedDropdownItems = _b.items, mappedValuePlaceholder = _b.placeholder, _c = _a.nextButton, nextButtonText = _c.text, nextDescription = _c.description, allowedDomain = _c.allowedDomain, iconType = _a.iconType, model = _a.model, formElementId = _a.id, error = _a.error;
        var existingValues = incomingValues || [];
        var nextUrlOrArray = integrationUtil_1.safeGetQsParam('next');
        var nextUrl = Array.isArray(nextUrlOrArray) ? nextUrlOrArray[0] : nextUrlOrArray;
        if (nextUrl && !nextUrl.startsWith(allowedDomain)) {
            // eslint-disable-next-line no-console
            console.warn("Got unexpected next url: " + nextUrl);
            nextUrl = undefined;
        }
        var _d = this.state, selectedSentryProjectId = _d.selectedSentryProjectId, selectedMappedValue = _d.selectedMappedValue;
        // create maps by the project id for constant time lookups
        var sentryProjectsById = Object.fromEntries(sentryProjects.map(function (project) { return [project.id, project]; }));
        var mappedItemsByValue = Object.fromEntries(mappedDropdownItems.map(function (item) { return [item.value, item]; }));
        // build sets of values used so we don't let the user select them twice
        var projectIdsUsed = new Set(existingValues.map(function (tuple) { return tuple[0]; }));
        var mappedValuesUsed = new Set(existingValues.map(function (tuple) { return tuple[1]; }));
        var projectOptions = sentryProjects
            .filter(function (project) { return !projectIdsUsed.has(project.id); })
            .map(function (_a) {
            var slug = _a.slug, id = _a.id;
            return ({ label: slug, value: id });
        });
        var mappedItemsToShow = mappedDropdownItems.filter(function (item) { return !mappedValuesUsed.has(item.value); });
        var handleSelectProject = function (_a) {
            var value = _a.value;
            _this.setState({ selectedSentryProjectId: value });
        };
        var handleSelectMappedValue = function (_a) {
            var value = _a.value;
            _this.setState({ selectedMappedValue: value });
        };
        var handleAdd = function () {
            // add the new value to the list of existing values
            var projectMappings = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(existingValues)), [
                [selectedSentryProjectId, selectedMappedValue],
            ]);
            // trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
            _this.setState({ selectedSentryProjectId: null, selectedMappedValue: null });
        };
        var handleDelete = function (index) {
            var projectMappings = removeAtArrayIndex_1.removeAtArrayIndex(existingValues, index);
            // trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
        };
        var renderItem = function (itemTuple, index) {
            var _a = tslib_1.__read(itemTuple, 2), projectId = _a[0], mappedValue = _a[1];
            var project = sentryProjectsById[projectId];
            // TODO: add special formatting if deleted
            var mappedItem = mappedItemsByValue[mappedValue];
            return (<Item key={index}>
          <MappedProjectWrapper>
            {project ? (<idBadge_1.default project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>) : (locale_1.t('Deleted'))}
            <icons_1.IconArrow size="xs" direction="right"/>
          </MappedProjectWrapper>
          <MappedItemValue>
            {mappedItem ? (<react_1.Fragment>
                <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
                {mappedItem.label}
                <StyledExternalLink href={mappedItem.url}>
                  <icons_1.IconOpen size="xs"/>
                </StyledExternalLink>
              </react_1.Fragment>) : (locale_1.t('Deleted'))}
          </MappedItemValue>
          <DeleteButtonWrapper>
            <button_1.default onClick={function () { return handleDelete(index); }} icon={<icons_1.IconDelete color="gray300"/>} size="small" type="button" aria-label={locale_1.t('Delete')}/>
          </DeleteButtonWrapper>
        </Item>);
        };
        var customValueContainer = function (containerProps) {
            // if no value set, we want to return the default component that is rendered
            var project = sentryProjectsById[selectedSentryProjectId || ''];
            if (!project) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
          <idBadge_1.default project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }} disableLink/>
        </react_select_1.components.ValueContainer>);
        };
        var customOptionProject = function (projectProps) {
            var project = sentryProjectsById[projectProps.value];
            // Should never happen for a dropdown item
            if (!project) {
                return null;
            }
            return (<react_select_1.components.Option {...projectProps}>
          <idBadge_1.default project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }} disableLink/>
        </react_select_1.components.Option>);
        };
        var customMappedValueContainer = function (containerProps) {
            // if no value set, we want to return the default component that is rendered
            var mappedValue = mappedItemsByValue[selectedMappedValue || ''];
            if (!mappedValue) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
          <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
          <OptionLabelWrapper>{mappedValue.label}</OptionLabelWrapper>
        </react_select_1.components.ValueContainer>);
        };
        var customOptionMappedValue = function (optionProps) {
            return (<react_select_1.components.Option {...optionProps}>
          <OptionWrapper>
            <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
            <OptionLabelWrapper>{optionProps.label}</OptionLabelWrapper>
          </OptionWrapper>
        </react_select_1.components.Option>);
        };
        return (<react_1.Fragment>
        {existingValues.map(renderItem)}
        <Item>
          <selectControl_1.default placeholder={locale_1.t('Sentry project\u2026')} name="project" options={projectOptions} components={{
                Option: customOptionProject,
                ValueContainer: customValueContainer,
            }} onChange={handleSelectProject} value={selectedSentryProjectId}/>
          <selectControl_1.default placeholder={mappedValuePlaceholder} name="mappedDropdown" options={mappedItemsToShow} components={{
                Option: customOptionMappedValue,
                ValueContainer: customMappedValueContainer,
            }} onChange={handleSelectMappedValue} value={selectedMappedValue}/>
          <AddProjectWrapper>
            <button_1.default type="button" disabled={!selectedSentryProjectId || !selectedMappedValue} size="small" priority="primary" onClick={handleAdd} icon={<icons_1.IconAdd />}/>
          </AddProjectWrapper>
          <FieldControlWrapper>
            {formElementId && (<div>
                <controlState_1.default model={model} name={formElementId}/>
                {error ? <StyledFieldErrorReason>{error}</StyledFieldErrorReason> : null}
              </div>)}
          </FieldControlWrapper>
        </Item>
        {nextUrl && (<NextButtonPanelAlert icon={false} type="muted">
            <NextButtonWrapper>
              {nextDescription !== null && nextDescription !== void 0 ? nextDescription : ''}
              <button_1.default type="button" size="small" priority="primary" icon={<icons_1.IconOpen size="xs" color="white"/>} href={nextUrl}>
                {nextButtonText}
              </button_1.default>
            </NextButtonWrapper>
          </NextButtonPanelAlert>)}
      </react_1.Fragment>);
    };
    return RenderField;
}(react_1.Component));
exports.RenderField = RenderField;
var ProjectMapperField = function (props) { return (<StyledInputField {...props} resetOnError inline={false} stacked={false} hideControlState field={function (renderProps) { return <RenderField {...renderProps}/>; }}/>); };
exports.default = ProjectMapperField;
var MappedProjectWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-right: ", ";\n"])), space_1.default(1));
var Item = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  min-height: 60px;\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2.5fr 2.5fr max-content 30px;\n  grid-template-areas: 'sentry-project mapped-value manage-project field-control';\n"], ["\n  min-height: 60px;\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2.5fr 2.5fr max-content 30px;\n  grid-template-areas: 'sentry-project mapped-value manage-project field-control';\n"])), space_1.default(2), function (p) { return p.theme.innerBorder; }, space_1.default(1));
var MappedItemValue = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  grid-gap: ", ";\n  width: 100%;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  grid-gap: ", ";\n  width: 100%;\n"])), space_1.default(1));
var DeleteButtonWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-area: manage-project;\n"], ["\n  grid-area: manage-project;\n"])));
var IntegrationIconWrapper = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var AddProjectWrapper = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  grid-area: manage-project;\n"], ["\n  grid-area: manage-project;\n"])));
var OptionLabelWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
var StyledInputField = styled_1.default(inputField_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var OptionWrapper = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  display: flex;\n"], ["\n  align-items: center;\n  display: flex;\n"])));
var FieldControlWrapper = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  grid-area: field-control;\n"], ["\n  position: relative;\n  grid-area: field-control;\n"])));
var NextButtonPanelAlert = styled_1.default(panels_1.PanelAlert)(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  margin-bottom: -1px;\n  border-bottom-left-radius: ", ";\n  border-bottom-right-radius: ", ";\n"], ["\n  align-items: center;\n  margin-bottom: -1px;\n  border-bottom-left-radius: ", ";\n  border-bottom-right-radius: ", ";\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var NextButtonWrapper = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(1));
var StyledFieldErrorReason = styled_1.default(fieldErrorReason_1.default)(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=projectMapperField.jsx.map