Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var scoreComponents = {
    'exception:message:character-shingles': locale_1.t('Exception Message'),
    'exception:stacktrace:pairs': locale_1.t('Stack Trace Frames'),
    'exception:stacktrace:application-chunks': locale_1.t('In-App Frames'),
    'message:message:character-shingles': locale_1.t('Log Message'),
    // v2
    'similarity:*:type:character-5-shingle': locale_1.t('Exception Type'),
    'similarity:*:value:character-5-shingle': locale_1.t('Exception Message'),
    'similarity:*:stacktrace:frames-pairs': locale_1.t('Stack Trace Frames'),
    'similarity:*:message:character-5-shingle': locale_1.t('Log Message'),
};
var SimilarScoreCard = function (_a) {
    var _b = _a.scoreList, scoreList = _b === void 0 ? [] : _b;
    if (scoreList.length === 0) {
        return null;
    }
    var sumOtherScores = 0;
    var numOtherScores = 0;
    return (<react_1.Fragment>
      {scoreList.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), key = _b[0], score = _b[1];
            var title = scoreComponents[key.replace(/similarity:\d\d\d\d-\d\d-\d\d/, 'similarity:*')];
            if (!title) {
                if (score !== null) {
                    sumOtherScores += score;
                    numOtherScores += 1;
                }
                return null;
            }
            return (<Wrapper key={key}>
            <div>{title}</div>
            <Score score={score === null ? score : Math.round(score * 4)}/>
          </Wrapper>);
        })}

      {numOtherScores > 0 && sumOtherScores > 0 && (<Wrapper>
          <div>{locale_1.t('Other')}</div>
          <Score score={Math.round((sumOtherScores * 4) / numOtherScores)}/>
        </Wrapper>)}
    </react_1.Fragment>);
};
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n"])), space_1.default(0.25));
var Score = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 16px;\n  width: 48px;\n  border-radius: 2px;\n  background-color: ", ";\n"], ["\n  height: 16px;\n  width: 48px;\n  border-radius: 2px;\n  background-color: ", ";\n"])), function (p) {
    return p.score === null ? p.theme.similarity.empty : p.theme.similarity.colors[p.score];
});
exports.default = SimilarScoreCard;
var templateObject_1, templateObject_2;
//# sourceMappingURL=similarScoreCard.jsx.map