echo -e "\n\n"
echo "============================================"
echo "ScriptExe.sh:Step1: Make Skim NanoAOD       "
echo "============================================"
cmsRun -j FrameworkJobReport.xml -p PSet.py
#
#
#
echo -e "\n\n"
echo "=========================================================="
echo "ScriptExe.sh:Step2: Make unskim NanoAOD for Runs Tree     "
echo "=========================================================="
cmsRun CustomPFNano_OnlyGenTableTask.py jobNumber=${1}
#
#
#
echo -e "\n\n"
echo "==========================================================="
echo "ScriptExe.sh:Step3: Removing Runs tree from tree.root      "
echo "==========================================================="
rootrm tree.root:Runs
#
#
#
echo -e "\n\n"
echo "=================================================================="
echo "ScriptExe.sh:Step4: Copy Runs tree from treeForRuns to tree.root  "
echo "=================================================================="
rootcp treeForRuns.root:Runs tree.root:Runs
