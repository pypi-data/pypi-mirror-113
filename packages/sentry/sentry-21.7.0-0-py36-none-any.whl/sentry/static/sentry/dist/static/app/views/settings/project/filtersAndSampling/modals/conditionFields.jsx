Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dynamicSampling_1 = require("app/types/dynamicSampling");
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var textareaField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textareaField"));
var legacyBrowsersField_1 = tslib_1.__importDefault(require("./legacyBrowsersField"));
var utils_1 = require("./utils");
function ConditionFields(_a) {
    var conditions = _a.conditions, categoryOptions = _a.categoryOptions, onAdd = _a.onAdd, onDelete = _a.onDelete, onChange = _a.onChange;
    var availableCategoryOptions = categoryOptions.filter(function (categoryOption) {
        return !conditions.find(function (condition) { return condition.category === categoryOption[0]; });
    });
    return (<Wrapper>
      {conditions.map(function (_a, index) {
            var match = _a.match, legacyBrowsers = _a.legacyBrowsers, category = _a.category;
            var selectedCategoryOption = categoryOptions.find(function (categoryOption) { return categoryOption[0] === category; });
            // selectedCategoryOption should be always defined
            var choices = selectedCategoryOption
                ? tslib_1.__spreadArray([selectedCategoryOption], tslib_1.__read(availableCategoryOptions)) : availableCategoryOptions;
            var displayLegacyBrowsers = category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER;
            var isMatchesDisabled = category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS ||
                category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST ||
                category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS ||
                displayLegacyBrowsers;
            return (<FieldsWrapper key={index}>
            <Fields>
              <selectField_1.default label={locale_1.t('Category')} 
            // help={t('This is a description')} // TODO(PRISCILA): Add correct description
            name={"category-" + index} value={category} onChange={function (value) { return onChange(index, 'category', value); }} choices={choices} inline={false} hideControlState showHelpInTooltip required stacked/>
              <textareaField_1.default label={locale_1.t('Matches')} 
            // help={t('This is a description')} // TODO(PRISCILA): Add correct description
            placeholder={utils_1.getMatchFieldPlaceholder(category)} name={"match-" + index} value={isMatchesDisabled ? '' : match} onChange={function (value) { return onChange(index, 'match', value); }} disabled={isMatchesDisabled} inline={false} rows={1} autosize hideControlState showHelpInTooltip flexibleControlStateSize required stacked/>
              <ButtonDeleteWrapper>
                <button_1.default onClick={onDelete(index)} size="small">
                  {locale_1.t('Delete Condition')}
                </button_1.default>
              </ButtonDeleteWrapper>
            </Fields>
            <IconDeleteWrapper onClick={onDelete(index)}>
              <icons_1.IconDelete aria-label={locale_1.t('Delete Condition')}/>
            </IconDeleteWrapper>
            {displayLegacyBrowsers && (<legacyBrowsersField_1.default selectedLegacyBrowsers={legacyBrowsers} onChange={function (value) {
                        onChange(index, 'legacyBrowsers', value);
                    }}/>)}
          </FieldsWrapper>);
        })}
      {!!availableCategoryOptions.length && (<StyledButton icon={<icons_1.IconAdd isCircled/>} onClick={onAdd} size="small">
          {locale_1.t('Add Condition')}
        </StyledButton>)}
    </Wrapper>);
}
exports.default = ConditionFields;
var IconDeleteWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 40px;\n  margin-top: 24px;\n  cursor: pointer;\n  display: none;\n  align-items: center;\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"], ["\n  height: 40px;\n  margin-top: 24px;\n  cursor: pointer;\n  display: none;\n  align-items: center;\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var Fields = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr;\n    grid-gap: ", ";\n  }\n"], ["\n  display: grid;\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr;\n    grid-gap: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(2));
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  > * {\n    :not(:first-child) {\n      label {\n        display: none;\n      }\n      ", " {\n        margin-top: 0;\n      }\n\n      ", " {\n        @media (max-width: ", ") {\n          border-top: 1px solid ", ";\n          padding-top: ", ";\n          margin-top: ", ";\n        }\n      }\n    }\n  }\n"], ["\n  > * {\n    :not(:first-child) {\n      label {\n        display: none;\n      }\n      ", " {\n        margin-top: 0;\n      }\n\n      ", " {\n        @media (max-width: ", ") {\n          border-top: 1px solid ", ";\n          padding-top: ", ";\n          margin-top: ", ";\n        }\n      }\n    }\n  }\n"])), IconDeleteWrapper, Fields, function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.border; }, space_1.default(2), space_1.default(2));
var FieldsWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var ButtonDeleteWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var StyledButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"], ["\n  margin: ", " 0;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=conditionFields.jsx.map