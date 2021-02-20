<?php
class Curl 
{
    public static function Get($uri, $content_type = "application/json")
    {
        $ch = curl_init();
            
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_URL, $uri);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Accept: $content_type",
            "Content-Type: $content_type",
            "User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0",
            "Authentication: 92540d8c662cc21c4bc70cd47bdc9505bf9eda96"
        ]);

        $out = curl_exec($ch);
        curl_close($ch);
        
        return $content_type == "application/json" ? new RecursiveIteratorIterator(new RecursiveArrayIterator(json_decode($out, true)), RecursiveIteratorIterator::SELF_FIRST) : $out;
    }

    
}

class GitCurl extends Curl
{
    public $_owner = null;
    
    public function __construct($_owner)
    {
        $this->_owner = $_owner;
    }

    private function Sanitize(array $arr, array $matchingFields) : array 
    {
        $out = [];
        foreach($arr as $set => $values)
            if(count($values) == count($matchingFields))
                $out[count($out)] = $values;

        return $out;
    }

    public function GetProfileData(array $fields) : array
    {
        $owner = $this->_owner;
        $results = [];
        foreach(parent::Get("https://api.github.com/users/${owner}") as $key => $value)
            if(in_array($key, $fields))
                $results[$key] = $value;

        return $results;
    }

    public function GetRepoData(array $fields, int $limit = -1) : array
    {
        $owner = $this->_owner;
        $out = array();
        $index = 0;
        $parsedLimit = $limit > 0 ? "?per_page=${limit}" : "";

        foreach(parent::Get("https://api.github.com/users/${owner}/repos${parsedLimit}") as $dataSet)
            if(is_array($dataSet))
            {
                foreach($dataSet as $key => $value)
                {
                    if(is_array($value)) 
                    {
                        $index++;
                        continue;
                    }

                    if(in_array($key, $fields))
                    {
                        $out[$index][$key] = $value;
                    }
                }
            }

        return $this->Sanitize($out, $fields);
    }

    public function RepoCount() : int
    {
        return $this->GetProfileData(["public_repos"])["public_repos"];
    }
    
    public function GetReadme(string $repo, string $branch = "master", string $owner = null) : string
    {
        $owner = $this->_owner;
        $uri = "https://raw.githubusercontent.com/${owner}/${repo}/${branch}/README.md";

        return parent::Get($uri, "text");
    }
}
?>
