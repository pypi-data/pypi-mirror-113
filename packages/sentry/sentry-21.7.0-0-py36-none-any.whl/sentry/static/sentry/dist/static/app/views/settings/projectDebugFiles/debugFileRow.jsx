Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var role_1 = tslib_1.__importDefault(require("app/components/acl/role"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("./utils");
var DebugFileRow = function (_a) {
    var debugFile = _a.debugFile, showDetails = _a.showDetails, downloadUrl = _a.downloadUrl, downloadRole = _a.downloadRole, onDelete = _a.onDelete;
    var id = debugFile.id, data = debugFile.data, debugId = debugFile.debugId, uuid = debugFile.uuid, size = debugFile.size, dateCreated = debugFile.dateCreated, objectName = debugFile.objectName, cpuName = debugFile.cpuName, symbolType = debugFile.symbolType, codeId = debugFile.codeId;
    var fileType = utils_1.getFileType(debugFile);
    var features = (data || {}).features;
    return (<react_1.Fragment>
      <Column>
        <div>
          <DebugId>{debugId || uuid}</DebugId>
        </div>
        <TimeAndSizeWrapper>
          <StyledFileSize bytes={size}/>
          <TimeWrapper>
            <icons_1.IconClock size="xs"/>
            <timeSince_1.default date={dateCreated}/>
          </TimeWrapper>
        </TimeAndSizeWrapper>
      </Column>
      <Column>
        <Name>
          {symbolType === 'proguard' && objectName === 'proguard-mapping'
            ? '\u2015'
            : objectName}
        </Name>
        <Description>
          <DescriptionText>
            {symbolType === 'proguard' && cpuName === 'any'
            ? locale_1.t('proguard mapping')
            : cpuName + " (" + symbolType + (fileType ? " " + fileType : '') + ")"}
          </DescriptionText>

          {features && (<FeatureTags>
              {features.map(function (feature) { return (<StyledTag key={feature} tooltipText={utils_1.getFeatureTooltip(feature)}>
                  {feature}
                </StyledTag>); })}
            </FeatureTags>)}
          {showDetails && (<div>
              {/* there will be more stuff here in the future */}
              {codeId && (<DetailsItem>
                  {locale_1.t('Code ID')}: {codeId}
                </DetailsItem>)}
            </div>)}
        </Description>
      </Column>
      <RightColumn>
        <buttonBar_1.default gap={0.5}>
          <role_1.default role={downloadRole}>
            {function (_a) {
            var hasRole = _a.hasRole;
            return (<tooltip_1.default disabled={hasRole} title={locale_1.t('You do not have permission to download debug files.')}>
                <button_1.default size="xsmall" icon={<icons_1.IconDownload size="xs"/>} href={downloadUrl} disabled={!hasRole}>
                  {locale_1.t('Download')}
                </button_1.default>
              </tooltip_1.default>);
        }}
          </role_1.default>
          <access_1.default access={['project:write']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<tooltip_1.default disabled={hasAccess} title={locale_1.t('You do not have permission to delete debug files.')}>
                <confirm_1.default confirmText={locale_1.t('Delete')} message={locale_1.t('Are you sure you wish to delete this file?')} onConfirm={function () { return onDelete(id); }} disabled={!hasAccess}>
                  <button_1.default priority="danger" icon={<icons_1.IconDelete size="xs"/>} size="xsmall" disabled={!hasAccess} data-test-id="delete-dif"/>
                </confirm_1.default>
              </tooltip_1.default>);
        }}
          </access_1.default>
        </buttonBar_1.default>
      </RightColumn>
    </react_1.Fragment>);
};
var DescriptionText = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-flex;\n  margin: 0 ", " ", " 0;\n"], ["\n  display: inline-flex;\n  margin: 0 ", " ", " 0;\n"])), space_1.default(1), space_1.default(1));
var FeatureTags = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-flex;\n  flex-wrap: wrap;\n  margin: -", ";\n"], ["\n  display: inline-flex;\n  flex-wrap: wrap;\n  margin: -", ";\n"])), space_1.default(0.5));
var StyledTag = styled_1.default(tag_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(0.5));
var Column = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"])));
var RightColumn = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n  margin-top: ", ";\n"])), space_1.default(1));
var DebugId = styled_1.default('code')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var TimeAndSizeWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n  align-items: center;\n"], ["\n  width: 100%;\n  display: flex;\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; }, space_1.default(1), function (p) { return p.theme.subText; });
var StyledFileSize = styled_1.default(fileSize_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  padding-left: ", ";\n"], ["\n  flex: 1;\n  padding-left: ", ";\n"])), space_1.default(0.5));
var TimeWrapper = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  flex: 2;\n  align-items: center;\n  padding-left: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  flex: 2;\n  align-items: center;\n  padding-left: ", ";\n"])), space_1.default(0.5), space_1.default(0.5));
var Name = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(1));
var Description = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  @media (max-width: ", ") {\n    line-height: 1.7;\n  }\n"], ["\n  font-size: ", ";\n  color: ", ";\n  @media (max-width: ", ") {\n    line-height: 1.7;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.breakpoints[2]; });
var DetailsItem = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  ", "\n  margin-top: ", "\n"], ["\n  ", "\n  margin-top: ", "\n"])), overflowEllipsis_1.default, space_1.default(1));
exports.default = DebugFileRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=debugFileRow.jsx.map